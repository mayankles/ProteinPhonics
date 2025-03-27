// components/midi_player/midi_player.js
(function() {
    // Create a container for the player UI.
    const container = document.getElementById("root");
    container.innerHTML = `
        <div id="midi-player">
            <button id="play-button">Play</button>
            <button id="pause-button" disabled>Pause</button>
        </div>
    `;

    // Use the global variable set in the HTML to get the MIDI file URL.
    const midiFileUrl = window.midi_file_url || "";
    if (!midiFileUrl) {
        console.error("No MIDI file URL provided.");
        container.innerHTML += "<p>Error: No MIDI file provided.</p>";
        return;
    }

    let player = null;
    try {
        player = new Tone.Player(midiFileUrl).toDestination();
    } catch (error) {
        console.error("Error creating Tone.Player:", error);
    }

    const playButton = document.getElementById("play-button");
    const pauseButton = document.getElementById("pause-button");

    playButton.addEventListener("click", async () => {
        if (player) {
            await Tone.start();
            player.start();
            playButton.disabled = true;
            pauseButton.disabled = false;
        }
    });

    pauseButton.addEventListener("click", () => {
        if (player) {
            player.stop();
            playButton.disabled = false;
            pauseButton.disabled = true;
        }
    });
})();
