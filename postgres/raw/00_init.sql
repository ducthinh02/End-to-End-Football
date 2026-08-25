
CREATE SCHEMA IF NOT EXISTS raw;
-- Lưu giữ dữ liệu bản sao của dữ liệu gốc 
-- Không chứa các join phức tạp và logic nghiệp vụ
-- Đóng vai trò là nguồn dữ liệu gốc duy nhất


CREATE SCHEMA IF NOT EXISTS staging;
-- Đóng vai trò vùng lưu giữ dữ liệu đã qua làm sạch và chuẩn hoá
-- Dữ liệu được lưu trong đây là dữ liệu đã được loại bỏ null đồng thời ép kiểu bắt buộc, tạo khoá thay thế, phi chuẩn hoá
-- Các bảng ở đây mang tính tạm thời/ phát sinh; các mô hình dbt được sử dụng dưới dạng view 
--     hoặc bảng tạm thời (ephemeral) để cung cấp dữ liệu cho analystics


CREATE SCHEMA IF NOT EXISTS analytics;
-- Ở đây gồm tầng trình bày (persentation) và tầng ngữ nghĩa (Semantic Layer) cho việc sử dụng cuối cùng (BI,jupyter notebook)
-- Được thiết kế theo mô hình star/snow (bảng fact_* và bảng dim_*), hoặc các bảng mở rộng đã được chọn lọc
-- Được thiết kế phù hợp với doanh nghiệp và có tính ổn định
-- Chỉ schema này mới được cấp quyền
