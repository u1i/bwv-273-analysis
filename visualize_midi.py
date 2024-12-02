import mido
import numpy as np
import plotly.graph_objects as go

def read_midi(file_path):
    midi_file = mido.MidiFile(file_path)
    notes_by_track = []
    
    for track_idx, track in enumerate(midi_file.tracks):
        notes = []
        current_time = 0
        
        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append((current_time, msg.note, track_idx))
        
        if notes:  # Only add tracks that have notes
            notes_by_track.extend(notes)
    
    return notes_by_track

def create_wave_visualization(notes):
    # Convert notes to numpy arrays for easier manipulation
    times = np.array([note[0] for note in notes])
    pitches = np.array([note[1] for note in notes])
    tracks = np.array([note[2] for note in notes])
    
    # Create color scale based on track numbers
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    names = ['Soprano', 'Alto', 'Tenor', 'Bass']
    
    # Create the figure
    fig = go.Figure()
    
    # Add traces for each track
    for track_idx in range(4):
        mask = tracks == track_idx + 1
        if np.any(mask):
            # Sort by time to ensure correct line connection
            sort_idx = np.argsort(times[mask])
            track_times = times[mask][sort_idx]
            track_pitches = pitches[mask][sort_idx]
            
            fig.add_trace(
                go.Scatter(
                    x=track_times,
                    y=track_pitches,
                    mode='lines+markers',
                    name=names[track_idx],
                    line=dict(color=colors[track_idx], width=2),
                    marker=dict(size=6)
                )
            )
    
    # Update layout
    def midi_to_note(midi_num):
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note_name = notes[midi_num % 12]
        octave = midi_num // 12 - 1
        return f'{note_name}{octave}'
    
    fig.update_layout(
        title='Bach MIDI Visualization - Voice Waves',
        xaxis_title='Time',
        yaxis_title='Pitch',
        yaxis=dict(
            tickmode='array',
            ticktext=[midi_to_note(n) for n in range(45, 76, 3)],
            tickvals=list(range(45, 76, 3))
        ),
        height=600,
        width=1200,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig

def main():
    # Read the MIDI file
    midi_path = 'bach.mid'
    notes = read_midi(midi_path)
    
    # Create and show the visualization
    fig = create_wave_visualization(notes)
    fig.show()

if __name__ == '__main__':
    main()
