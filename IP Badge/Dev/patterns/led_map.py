# Not 100% sure this is accurate but I'm tired
# Individual sections
left_sky = [0, 1, 2, 3, 4, 5, 6]
right_sky = [59, 60, 61, 62, 63, 64, 65, 66]
bottom = [67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82]

beam = [7, 8, 9, 10, 11, 12]
eye = [25,26,27]
triangle_upper_mid = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
triangle_center_ring = [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
triangle_lower_mid = [30, 31, 32, 33, 34, 35, 36, 37]
triangle_left = [38, 39, 40, 41, 42, 43]
triangle_right = [44, 45, 46, 47, 48, 49]
triangle_lower = [50, 51, 52, 53, 54, 55, 56, 57]
triangle_tip = [58]
triangle_bottom_wings = [59, 60, 61]

# Combined groups
triangle = (
    triangle_upper_mid + triangle_center_ring +
    triangle_lower_mid + triangle_left + triangle_right +
    triangle_lower + triangle_tip + triangle_bottom_wings
)

sky = left_sky + right_sky
full = left_sky + right_sky + triangle + bottom

# All LEDs
all_leds = list(range(83))