# Not 100% sure this is accurate but I'm tired, numbering starts a zero
# Individual sections
left_sky = [0, 1, 2, 3, 4, 5, 6] # AKA left glitch
right_sky = [60, 61, 62, 63, 64, 65, 66, 67] # AKA right glitch
bottom = [68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82]
beam = [7, 8, 9, 10, 11, 12] # This is from the UFO to the top of the pyramid
eye = [27,28,29]
skull = [53]

# Triangle sections
triangle_center_tip = [13, 14, 17] # Very top center of pyramid
triangle_eye_ring = [19,22,23,32,33,37,43,51,52,55] # the diamond shape around eye, extends to bottom of triangle
triangle_left_outter = [15,18,21,25,26,34,35,46,47,48]
triangle_left_inner = [36,41,42,49,50]
triangle_right_outter = [16,20,24,30,31,39,40,57,58,59]
triangle_right_inner = [38,44,45,54,56]

triangle = (triangle_center_tip + triangle_eye_ring + eye +
                 triangle_left_outter + triangle_left_inner +
                 triangle_right_inner + triangle_right_outter + skull
)

sky = left_sky + right_sky
center_beam = (beam + triangle_center_tip + triangle_eye_ring + 
               triangle_left_inner + triangle_right_inner)
center_w_bottom = center_beam + bottom
beam_w_triangle = (center_beam + triangle)
full = left_sky + right_sky + eye + skull + bottom + triangle

# All LEDs
all_leds = list(range(90))