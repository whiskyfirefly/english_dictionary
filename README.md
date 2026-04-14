# 📚 English Dictionary với Radix Trie Visualizer

Ứng dụng từ điển tiếng Anh tương tác sử dụng **Radix Trie** - cấu trúc dữ liệu tối ưu cho tìm kiếm prefix nhanh.

**✨ Nổi bật**: 
- Giao diện **2 cột**: Tìm kiếm/Thêm/Xóa từ (trái) ↔ Tree Visualization (phải)
- **Visualize cây Radix Trie real-time** với màu sắc theo độ sâu

---

## 🎯 Tính Năng Chính

### 1. **Tìm Kiếm Từ (Search)**
- Tìm kiếm định nghĩa của một từ tiếng Anh
- Hiển thị cách phát âm (IPA)
- Hiển thị ví dụ sử dụng từ
- Gợi ý từ tự động khi gõ, tối đa 8 gợi ý, sắp xếp bảng chữ cái

### 2. **Thêm Từ Mới (Add)**
- Thêm từ mới vào từ điển
- Nhập định nghĩa tiếng Việt
- Nhập cách phát âm (IPA)
- Nhập danh sách ví dụ (cách nhau bằng `;`)

### 3. **Xóa Từ (Delete)**
- Xóa một từ khỏi từ điển (lưu ý, hệ thống sẽ không xóa hẳn mà chỉ đánh dấu là đã xóa để đảm bảo tính an toàn)
- Xác nhận trước khi xóa

---

## 📁 Cấu Trúc Dự Án

```
eng_dictionary/
├── README.md              # Tài liệu hướng dẫn (file này)
├── requirements.txt       # Danh sách thư viện Python cần cài đặt
├── server.py             # Backend - Flask server & API endpoints
├── trie.py               # Radix Trie data structure implementation
├── index.html            # Frontend - Giao diện web
├── script.js             # JavaScript - Logic tương tác người dùng
├── style.css             # CSS - Tạo kiểu cho giao diện
```

## 🚀 Cài Đặt & Hướng Dẫn Chạy

### 1️⃣ **Yêu Cầu Hệ Thống**

- Python 3.7 trở lên
- pip (Package manager cho Python)

### 2️⃣ **Cài Đặt Thư Viện**

```bash
# Mở terminal/command prompt tại thư mục eng_dictionary
cd eng_dictionary

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

**Thư viện sẽ cài đặt:**
- `flask` - Web framework để tạo server
- `flask-cors` - Hỗ trợ CORS nếu cần

**Thư viện frontend (tự động load từ CDN):**
- `vis.js` - Thư viện vẽ graph/network visualization
- `Font Awesome` - Icons

### 3️⃣ **Chạy Ứng Dụng**

```bash
# Chạy server Flask
python server.py
```

**Output dự kiến:**
```
 * Serving Flask app 'server'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### 4️⃣ **Truy Cập Ứng Dụng**

Mở trình duyệt web và truy cập:
```
http://localhost:5000
```

Hoặc:
```
http://127.0.0.1:5000
```

---

## 📖 Hướng Dẫn Sử Dụng

### **Tìm Kiếm Từ**
1. Nhập từ trong ô input "Nhập từ cần tra cứu..."
2. Nhấn nút "Tìm kiếm" hoặc phím Enter
3. Xem kết quả: định nghĩa, phát âm, ví dụ

### **Xem Gợi Ý**
1. Bắt đầu gõ từ trong ô input
2. Danh sách gợi ý sẽ xuất hiện tự động
3. Click vào một gợi ý để chọn nó

### **Thêm Từ Mới**
1. Click nút "Thêm từ khóa cho từ điển"
2. Nhập thông tin:
   - **Word**: Từ tiếng Anh (bắt buộc)
   - **Definition**: Định nghĩa tiếng Việt (bắt buộc)
   - **Pronunciation**: Phiên âm (tùy chọn)
   - **Examples**: Ví dụ, cách nhau bằng `;` (tùy chọn)
3. Click "Lưu" để lưu từ, "Hủy" để hủy việc thêm"

### **Xóa Từ**
1. Tìm kiếm từ cần xóa
2. Click nút "Delete" trong kết quả
3. Xác nhận xóa trong hộp thoại

---

## 📝 Từ Điển Mặc Định

Ứng dụng đi kèm với 13 từ mặc định:

| Từ | Định Nghĩa | Phát Âm |
|---|---|---|
| hello | Lời chào hỏi | /həˈloʊ/ |
| world | Trái đất | /wɜːrld/ |
| python | Ngôn ngữ lập trình | /ˈpaɪθɑːn/ |
| dictionary | Từ điển | /ˈdɪkʃəneri/ |
| radix | Cơ số, trie nén | /ˈreɪdɪks/ |
| trie | Cấu trúc dữ liệu cây | /traɪ/ |
| search | Tìm kiếm | /sɜːrtʃ/ |
| add | Thêm | /æd/ |
| delete | Xóa | /dɪˈliːt/ |
| data | Dữ liệu | /ˈdeɪtə/ |
| happy | Vui vẻ | /ˈhæpi/ |
| harmony | Hòa hợp | /ˈhɑːrməni/ |
| hint | Gợi ý | /hɪnt/ |
---

## 🌳 Cách Hoạt Động của Tree Visualization
1. **Page Load**: JavaScript gọi `/api/tree` để lấy cấu trúc cây
2. **Render**: vis.js vẽ graph với nodes và edges
3. **Tương tác**: 
   - Khi **tìm kiếm** từ → Tree cập nhật (node liên quan highlight tô màu vàng)
   - Khi **thêm từ** → Tree thêm node mới tự động
   - Khi **xóa từ** → Tree đánh dấu node đó là đã xóa (node liên quan được highlight màu đỏ)
4. **Visual Feedback**: Màu sắc khác nhau giúp phân biệt loại node

---

## 🔧 Tệp Chi Tiết
### **server.py** - Flask Backend
**Endpoints:**
- `GET /` - Trang chủ (index.html)
- `GET /api/search` - Tìm kiếm từ (HTTP 404 nếu không tìm thấy)
- `POST /api/add` - Thêm từ (HTTP 409 nếu từ tồn tại + `is_deleted = false`)
- `POST /api/delete` - Xóa từ (set `is_deleted = true`)
- `GET /api/suggestions` - Gợi ý từ theo prefix (max 20)
- `GET /api/tree` - Cấu trúc cây cho vis.js (JSON nodes + edges)

**Validation:**
- HTTP 409: Từ đã tồn tại khi `is_deleted = false`
- HTTP 404: Từ không tìm thấy
- HTTP 400: Thiếu dữ liệu bắt buộc

---

## 🐛 Khắc Phục Sự Cố

### **Lỗi: "Command 'python' not found"**
Dùng `python3`:
```bash
python3 server.py
```

### **Lỗi: "ModuleNotFoundError: No module named 'flask'"**
Cài đặt lại:
```bash
pip install -r requirements.txt
```

### **Port 5000 đã được dùng**
Sửa `server.py`, dòng cuối:
```python
app.run(debug=True, port=5001)  # Đổi port
```

### **Tree không cập nhật sau khi thêm/xóa từ**
1. F12 mở Console kiểm tra lỗi JavaScript
2. Kiểm tra Flask server chạy bình thường (terminal)
3. Xóa browser cache: Ctrl+Shift+Delete


---

## ❓ Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra console browser (F12)
2. Kiểm tra terminal nơi chạy server
3. Đọc kỹ thông báo lỗi
---

## 🔗 API Endpoints

Ứng dụng cung cấp các endpoint REST API:

### **GET /api/search**
Tìm kiếm từ trong từ điển
```bash
curl "http://localhost:5000/api/search?word=hello"
```
**Response:**
```json
{
  "word": "hello",
  "definition": "Lời chào hỏi hoặc để bắt đầu cuộc trò chuyện",
  "examples": ["Hello, how are you today?"],
  "pronunciation": "/həˈloʊ/"
}
```

### **POST /api/add**
Thêm từ mới vào từ điển
```bash
curl -X POST "http://localhost:5000/api/add" \
  -H "Content-Type: application/json" \
  -d '{
    "word": "awesome",
    "definition": "Rất tuyệt vời",
    "examples": ["That movie is awesome"],
    "pronunciation": "/ɔːˈsʌm/"
  }'
```

### **POST /api/delete**
Xóa từ khỏi từ điển
```bash
curl -X POST "http://localhost:5000/api/delete" \
  -H "Content-Type: application/json" \
  -d '{"word": "hello"}'
```

### **GET /api/suggestions**
Lấy gợi ý từ dựa trên tiền tố
```bash
curl "http://localhost:5000/api/suggestions?prefix=hap"
```
**Response:**
```json
{
  "words": ["happy", "harmony"]
}
```

### **GET /api/tree** (NEW!)
Lấy cấu trúc cây Radix Trie dưới dạng nodes và edges (dành cho vis.js):
```bash
curl "http://localhost:5000/api/tree"
```
**Response (example):**
```json
{
  "nodes": [
    {"id": 0, "label": "ROOT", "color": "#FF9800", "size": 40},
    {"id": 1, "label": "hello", "title": "hello", "color": "#4CAF50", "size": 35},
    ...
  ],
  "edges": [
    {"from": 0, "to": 1},
    ...
  ]
}
```


