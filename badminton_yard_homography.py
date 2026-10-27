import cv2
import numpy as np

# Danh sách lưu trữ 4 điểm click chuột
pts_src = []

def click_event(event, x, y, flags, param):
    global pts_src
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(pts_src) < 4:
            pts_src.append([x, y])
            print(f"Đã chọn điểm thứ {len(pts_src)}: x={x}, y={y}")
            # Vẽ một chấm tròn nhỏ tại điểm vừa click để dễ nhìn
            cv2.circle(img_display, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow("Chon 4 goc san", img_display)

# 1. Đọc ảnh gốc
img = cv2.imread("badminton_yard.jpg")
if img is None:
    print("Không tìm thấy file ảnh badminton_yard.jpg!")
    exit()

img_display = img.copy()
cv2.imshow("Chon 4 goc san", img_display)
cv2.setMouseCallback("Chon 4 goc san", click_event)

print("HƯỚNG DẪN:")
print("Hãy click lần lượt vào 4 góc của sân trên cửa sổ ảnh theo thứ tự:")
print("1. Top-Left (Góc trên bên trái)")
print("2. Top-Right (Góc trên bên phải)")
print("3. Bottom-Right (Góc dưới bên phải)")
print("4. Bottom-Left (Góc dưới bên trái)")
print("Sau khi click đủ 4 điểm, hãy bấm phím bất kỳ để tiếp tục...")

cv2.waitKey(0)
cv2.destroyAllWindows()

# Kiểm tra xem đã click đủ 4 điểm chưa
if len(pts_src) == 4:
    pts_src = np.float32(pts_src)
    
    # Khai báo kích thước chuẩn 2D cho sân cầu lông (Tỷ lệ 6.1m x 13.4m)
    width, height = 305, 670
    pts_dst = np.float32([
        [0, 0],                  # Top-Left
        [width - 1, 0],          # Top-Right
        [width - 1, height - 1], # Bottom-Right
        [0, height - 1]          # Bottom-Left
    ])

    # Tính toán ma trận Homography và nắn ảnh
    H, _ = cv2.findHomography(pts_src, pts_dst)
    tactical_view = cv2.warpPerspective(img, H, (width, height))

    # Lưu ảnh kết quả vào file
    output_filename = "tactical_view_output.jpg"
    cv2.imwrite(output_filename, tactical_view)
    print(f"Đã lưu ảnh thành công vào file: {output_filename}")

    # Hiển thị kết quả ảnh đã căn đều
    cv2.imshow("Tactical View (2D - Can Chinh)", tactical_view)
    print("Đã nắn ảnh thành công! Bấm phím bất kỳ để thoát.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Bạn chưa click đủ 4 điểm. Vui lòng chạy lại chương trình!")