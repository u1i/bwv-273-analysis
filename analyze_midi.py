import mido

def analyze_midi(file_path):
    midi_file = mido.MidiFile(file_path)
    print(f"MIDI File Analysis for {file_path}")
    print(f"Number of tracks: {len(midi_file.tracks)}")
    print(f"Ticks per beat: {midi_file.ticks_per_beat}")
    
    notes = []
    velocities = set()
    
    for i, track in enumerate(midi_file.tracks):
        print(f"\nTrack {i}: {track.name if hasattr(track, 'name') else 'Unnamed'}")
        print(f"Number of messages: {len(track)}")
        
        current_time = 0
        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append((current_time, msg.note, msg.velocity))
                velocities.add(msg.velocity)
    
    if notes:
        print("\nVelocity Analysis:")
        print(f"Unique velocities found: {sorted(velocities)}")
        print(f"Total notes: {len(notes)}")

if __name__ == '__main__':
    analyze_midi('bach.mid')
