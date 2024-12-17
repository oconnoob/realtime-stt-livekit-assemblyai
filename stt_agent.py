import asyncio
import logging

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    stt,
    transcription,
)
from livekit.plugins import assemblyai

load_dotenv()

logger = logging.getLogger("transcriber")

async def entrypoint(ctx: JobContext):
    logger.info(f"Starting transcriber (speech to text) example, room: {ctx.room.name}")
    stt_impl = assemblyai.STT()

    @ctx.room.on("track_subscribed")
    def on_track_subscribed(
        track: rtc.Track,
        publication: rtc.TrackPublication,
        participant: rtc.RemoteParticipant,
    ):
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            asyncio.create_task(transcribe_track(participant, track))

    async def transcribe_track(participant: rtc.RemoteParticipant, track: rtc.Track):
        """
        Handles the parallel tasks of sending audio to the STT service and 
        forwarding transcriptions back to the app.
        """
        audio_stream = rtc.AudioStream(track)
        stt_forwarder = transcription.STTSegmentsForwarder(
            room=ctx.room, participant=participant, track=track
        )

        stt_stream = stt_impl.stream()

        # Run tasks for audio input and transcription output in parallel
        await asyncio.gather(
            _handle_audio_input(audio_stream, stt_stream),
            _handle_transcription_output(stt_stream, stt_forwarder),
        )

    async def _handle_audio_input(
        audio_stream: rtc.AudioStream, stt_stream: stt.SpeechStream
    ):
        """Pushes audio frames to the speech-to-text stream."""
        async for ev in audio_stream:
            stt_stream.push_frame(ev.frame)

    async def _handle_transcription_output(
        stt_stream: stt.SpeechStream, stt_forwarder: transcription.STTSegmentsForwarder
    ):
        """Receives transcription events from the speech-to-text service."""
        async for ev in stt_stream:
            if ev.type == stt.SpeechEventType.FINAL_TRANSCRIPT:
                print(" -> ", ev.alternatives[0].text)

            stt_forwarder.update(ev)

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
