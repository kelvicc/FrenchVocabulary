# -*- coding: utf-8 -*-
import os
import asyncio
import edge_tts

AUDIO_DIR = r"c:\Users\noid\Documents\antigravity\kind-fermi\duo_francais\audio"

async def main():
    dot_mp3 = os.path.join(AUDIO_DIR, ".mp3")
    if os.path.exists(dot_mp3):
        os.remove(dot_mp3)
        print("Removed .mp3")

    text = "Malgré la grève des transports, Claire a réussi à arriver à l'heure au bureau en pédalant sous la pluie."
    target = os.path.join(AUDIO_DIR, "sentence_011.mp3")

    # Generate with Vivienne
    comm = edge_tts.Communicate(text, "fr-FR-VivienneMultilingualNeural")
    await comm.save(target)
    print("Generated sentence_011.mp3 with Vivienne. Size:", os.path.getsize(target))

if __name__ == "__main__":
    asyncio.run(main())
