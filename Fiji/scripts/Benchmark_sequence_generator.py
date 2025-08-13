# Mastodon Benchmark Sequence Generator
# Generates BDV_T / BDV_R / Zoom command sequences for benchmarking a .mastodon project.

# Parameters for regular_vs_irregular
timepoint_span = range(1, 20)    # Timepoints
max_bookmarks = 3                # TrackScheme Bookmarks: TS_B1 TS_B2 TS_B3
rotation_step = 5                # Rotation amount: BDV_R<number>
rotation_interval = 1            # Include BDV_R every Nth BDV_T event (1 = every, 2 = every 2nd, etc.)
bdv_t_frequency = 1              # Frequency of BDV_T (e.g., every N timepoints)
zoom_x = 1                       # Zoom Position 1
zoom_y = 3                       # Zoom Position 2
zoom_frames = 10                 # Frames for zoom transition

# Toggles
include_bdv_fcentre = False      # Toggle BDV_Fcentre: requires a spot labeled 'centre' in the Mastodon project.
                                 # You can generate it by going to the TrackScheme view, selecting all spots and links (Ctrl + A),
                                 # then using Plugins > Spots management > Transform spots > Add center spots.
include_bookmarks = False        # Toggle bookmarks
include_rotation = False         # Toggle rotation
include_zoom_in = False          # Toggle zoom-in command
include_zoom_out = False         # Toggle zoom-out command

# Precompute static elements
zoom_in_command = "TS_Z"+str(zoom_x)+"-"+str(zoom_y)+"-"+str(zoom_frames) if include_zoom_in else ""
zoom_out_command = "TS_Z"+str(zoom_y)+"-"+str(zoom_x)+"-"+str(zoom_frames) if include_zoom_out else ""

# Helper: Determine whether this index triggers a BDV_T event
def is_bdv_t_step(idx):
    return idx % bdv_t_frequency == 0

# Generate the pattern
output_elements = []

for idx, t in enumerate(timepoint_span):
    if not is_bdv_t_step(idx):
        continue  # Only process steps aligned with BDV_T frequency

    components = []

    # Step 1: BDV_T and optional BDV_Fcentre
    components.append("BDV_T"+str(t))
    if include_bdv_fcentre:
        components.append("BDV_Fcentre")

    # Step 2: Bookmarks
    if include_bookmarks:
        components.extend(["TS_B"+str(i) for i in range(1, max_bookmarks + 1)])

    # Step 3: Rotation
    if include_rotation and (idx // bdv_t_frequency) % rotation_interval == 0:
        components.append("BDV_R"+str(rotation_step))

    # Step 4: Zoom commands
    if include_zoom_in:
        components.append(zoom_in_command)
    if include_zoom_out:
        components.append(zoom_out_command)

    output_elements.append(" ".join(filter(None, components)))

# Final output (single line for Mastodon)
final_output = " ".join(output_elements)

# Save to file
output_filename = "benchmark_sequence.txt"
with open(output_filename, "w") as f:
    f.write(final_output)

# --- Print Output ---
print("\n--- Mastodon Benchmark Sequence (Single Line) ---")
print("Copy the entire line below into Mastodon's benchmark commands field as a single line:")
print("\n" + final_output)

print("\n--- Multi-Line View (For Readability Only) ---")
for line in output_elements:
    print(line)

print("\nSequence also saved to: "+output_filename)

