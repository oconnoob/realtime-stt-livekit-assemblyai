# Real-time Speech-to-Text in LiveKit with AssemblyAI

This repository contains a minimal example of how to use AssemblyAI's real-time transcription API with LiveKit. See the companion blog [**How to add real-time Speech-to-Text to your LiveKit application**](https://www.assemblyai.com/blog/livekit-realtime-speech-to-text) for a full walkthrough.

![demo](demo.gif)

See the companion blog for more detailed instructions on how to set up and run this example, but here is the general overview:

1. Clone this repository and `cd` into it
2. Rename `.env.example` to `.env`
3. Go to [livekit.io](https://livekit.io) and sign up for free
4. In your LiveKit dashboard, go to `Settings > Keys` and click on your API key
5. Copy the URL, API key, and secret values into the `.env` file
6. Go to [assemblyai.com](https://www.assemblyai.com/dashboard/signup?utm_source=blog&utm_medium=internal-link&utm_campaign=livekit-realtime-speech-to-text) to sign up for free
7. Copy your AssemblyAI API key into the `.env` file
8. `pip install -r requirements.txt` to install requirements
9. `python stt_agent.py` to run the Speech-to-Text agent
10. Go the the [LiveKit Agents Playground](https://agents-playground.livekit.io/) and sign in with your LiveKit account. Begin speaking and you will see your speech transcribed in real-time both in the Playground and in the agent's terminal.
