# Mastodon Benchmark Sequence Generator
# Generates BDV_T / BDV_R / Zoom command sequences for benchmarking a .mastodon project.

# Parameters for regular_vs_irregular
#@(label="Time point range from (inclusive):", min="0") int timepoint_span_from = 1
#@(label="Time point range till (inclusive):", min="0") int timepoint_span_till = 20
timepoint_span = range(timepoint_span_from, timepoint_span_till+1)
#@(label="Skip time points:", description="Period between commands (e.g., every N timepoints)", min="0") int bdv_t_frequency = 1
bdv_t_frequency += 1

# TODO: Here, message in the dialog what happens at every non-skipped time point.

# Toggle BDV_Fcentre: requires a spot labeled 'centre' in the Mastodon project.
# You can generate it by going to the TrackScheme view, selecting all spots and links (Ctrl + A),
# then using Plugins > Spots management > Transform spots > Add center spots.
#@(label="Do BDV_Fcentre:", description="At every time point do this command.") boolean include_bdv_fcentre = False

# TODO: Message that 'centre' spot needs to exist at the visited spots.

#@(label="Do BDV rotations:", description="Include BDV rotations into the generated sequence, or not at all.") boolean include_rotation = False
#@(label="Rotation with Nth time point:", description="Include BDV_R with every Nth visited time point (1 = every, 2 = every 2nd, etc.)") int rotation_interval = 1
#@(label="Rotation steps:", description="Use BDV_R<steps> in every BDV_R command in the generated sequence.") int rotation_step = 5

#@(label="Do visit TS bookmarks:", description="Includes TS bookmarks into the generated sequence.") boolean include_bookmarks = False
#@(label="Number of TS bookmarks:", description="How long sequence of TS_B1 TS_B2 TS_B3... to use per time point.") int max_bookmarks = 3

#@(label="Do TS zoom-in (pos 1 -> 2):", description="Enable/disable zoom-in command in the generated sequence.") boolean include_zoom_in = False
#@(label="Do TS zoom-out (pos 2 -> 1):", description="Enable/disable zoom-out command in the generated sequence.") boolean include_zoom_out = False
#@(label="TS zoom position 1:", description="Starting position for zoom-in, ending position for zoom-out.") int zoom_x = 1
#@(label="TS zoom position 2:", description="Ending position for zoom-in, starting position for zoom-out.") int zoom_y = 3
#@(label="TS zoom frames:", description="Number of frames for the zoom transition") int zoom_frames = 10



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

