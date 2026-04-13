from flask import Flask, jsonify, request, render_template
from trie import RadixTrie
import json
import os

# Khởi tạo Flask app
app = Flask(__name__, static_folder='.', static_url_path='', template_folder='.')
# Khởi tạo cây Radix Trie cho từ điển
dictionary = RadixTrie()

# ============================================================================
# Dữ liệu từ điển cơ bản - Định nghĩa tiếng Việt, ví dụ, cách phát âm
# ============================================================================
BASIC_WORDS = {
    "hello": {
        "definition": "Lời chào hỏi hoặc để bắt đầu cuộc trò chuyện",
        "examples": ["Hello, how are you today?"],
        "pronunciation": "/həˈloʊ/"
    },
    "world": {
        "definition": "Trái đất và toàn bộ cộng đồng loài người",
        "examples": ["Welcome to the world of programming"],
        "pronunciation": "/wɜːrld/"
    },
    "python": {
        "definition": "Ngôn ngữ lập trình bậc cao, dễ học",
        "examples": ["Python is great for data science"],
        "pronunciation": "/ˈpaɪθɑːn/"
    },
    "dictionary": {
        "definition": "Cuốn sách hoặc tài nguyên điện tử liệt kê các từ theo thứ tự bảng chữ cái",
        "examples": ["Look up the word in the dictionary"],
        "pronunciation": "/ˈdɪkʃəneri/"
    },
    "radix": {
        "definition": "Cơ số của hệ thống số; cấu trúc dữ liệu trie nén",
        "examples": ["Radix trees are memory efficient"],
        "pronunciation": "/ˈreɪdɪks/"
    },
    "trie": {
        "definition": "Cấu trúc dữ liệu cây để lưu trữ chuỗi với tìm kiếm nhanh",
        "examples": ["The trie is useful for prefix searches"],
        "pronunciation": "/traɪ/"
    },
    "search": {
        "definition": "Hành động tìm kiếm cẩn thận để tìm thứ gì đó",
        "examples": ["I searched for the word in the dictionary"],
        "pronunciation": "/sɜːrtʃ/"
    },
    "add": {
        "definition": "Đặt một cái gì đó cùng nhau với cái khác",
        "examples": ["Add the new word to the dictionary"],
        "pronunciation": "/æd/"
    },
    "delete": {
        "definition": "Loại bỏ hoặc xóa bỏ cái gì đó",
        "examples": ["Delete the incorrect word from the list"],
        "pronunciation": "/dɪˈliːt/"
    },
    "data": {
        "definition": "Các sự kiện và thống kê được thu thập để tham khảo hoặc phân tích",
        "examples": ["The data shows increasing trends"],
        "pronunciation": "/ˈdeɪtə/"
    },
    "happy": {
        "definition": "Cảm thấy hoặc thể hiện niềm vui và sự thỏa mãn",
        "examples": ["I am very happy today"],
        "pronunciation": "/ˈhæpi/"
    },
    "harmony": {
        "definition": "Sự kết hợp hòa hợp của các phần khác nhau",
        "examples": ["The team works in perfect harmony"],
        "pronunciation": "/ˈhɑːrməni/"
    },
    "hint": {
        "definition": "Một gợi ý hoặc tín hiệu tinh tế",
        "examples": ["Give me a hint to solve this problem"],
        "pronunciation": "/hɪnt/"
    },
}

def load_dictionary():
    """Tải tất cả từ cơ bản vào cây Radix Trie"""
    for word, data in BASIC_WORDS.items():
        dictionary.insert(
            word,
            definition=data.get("definition"),
            examples=data.get("examples"),
            pronunciation=data.get("pronunciation")
        )

# Tải từ điển khi ứng dụng khởi động
load_dictionary()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """Trả về trang chủ - giao diện web"""
    return render_template('index.html')

@app.route('/api/search')
def search():
    """
    API: Tìm kiếm từ trong từ điển
    Query params: word (chuỗi từ cần tìm)
    Response: JSON với thông tin từ (định nghĩa, ví dụ, phát âm)
    """
    word = request.args.get('word', '').strip().lower()
    
    if not word:
        return jsonify({"error": "Vui lòng nhập một từ"}), 400
    
    # Lấy thông tin từ từ trie
    word_data = dictionary.get_definition(word)
    
    if word_data is None:
        return jsonify({"error": f"Từ '{word}' không tìm thấy trong từ điển"}), 404
    
    return jsonify({
        "word": word,
        "definition": word_data.get("definition"),
        "examples": word_data.get("examples", []),
        "pronunciation": word_data.get("pronunciation", "")
    })

@app.route('/api/add', methods=['POST'])
def add_word():
    """
    API: Thêm từ mới vào từ điển
    Request body: JSON với word, definition, pronunciation (tùy chọn), examples (tùy chọn)
    Response: Thông báo thành công hoặc lỗi
    """
    data = request.get_json()
    
    # Lấy dữ liệu từ request
    word = data.get('word', '').strip().lower()
    definition = data.get('definition', '').strip()
    examples = data.get('examples', [])
    pronunciation = data.get('pronunciation', '').strip()
    
    # Kiểm tra dữ liệu bắt buộc
    if not word or not definition:
        return jsonify({"error": "Từ và định nghĩa là bắt buộc"}), 400
    
    # Kiểm tra từ đã tồn tại
    if dictionary.search(word):
        return jsonify({"error": f"Từ '{word}' đã tồn tại"}), 409
    
    # Thêm từ vào trie
    dictionary.insert(word, definition, examples, pronunciation)
    return jsonify({"message": f"Từ '{word}' được thêm thành công"}), 201

@app.route('/api/delete', methods=['POST'])
def delete_word():
    """
    API: Xóa từ khỏi từ điển
    Request body: JSON với word (từ cần xóa)
    Response: Thông báo thành công hoặc lỗi
    """
    data = request.get_json()
    word = data.get('word', '').strip().lower()
    
    if not word:
        return jsonify({"error": "Vui lòng nhập từ cần xóa"}), 400
    
    # Xóa từ từ trie
    if dictionary.delete(word):
        return jsonify({"message": f"Từ '{word}' được xóa thành công"}), 200
    else:
        return jsonify({"error": f"Từ '{word}' không tìm thấy"}), 404

def _collect_words_from_node(node, prefix):
    """
    Helper: Duyệt cây để thu thập tất cả từ
    - node: nút hiện tại
    - prefix: tiền tố hiện tại
    - Return: danh sách các từ bắt đầu từ nút này
    """
    words = []
    for edge, child in node.children.items():
        new_prefix = prefix + edge
        if child.is_end_of_word:
            words.append(new_prefix)
        words.extend(_collect_words_from_node(child, new_prefix))
    return words

@app.route('/api/all')
def get_all_words():
    """
    API: Lấy tất cả từ trong từ điển
    Response: JSON danh sách các từ đã sắp xếp bảng chữ cái
    """
    words = _collect_words_from_node(dictionary.root, "")
    return jsonify({"words": sorted(words)})

@app.route('/api/suggestions')
def get_suggestions():
    """
    API: Gợi ý từ dựa trên tiền tố (prefix)
    Query params: prefix (tiền tố cần tìm gợi ý)
    Response: Danh sách 8 từ gợi ý đã sắp xếp bảng chữ cái
    """
    prefix = request.args.get('prefix', '').strip().lower()
    
    if not prefix:
        return jsonify({"words": []}), 200
    
    def collect_suggestions(node, current_prefix, suggestions, max_count=20):
        """
        Duyệt cây để tìm gợi ý khớp với prefix
        - node: nút hiện tại
        - current_prefix: tiền tố hiện tại
        - suggestions: danh sách kết quả (pass by reference)
        - max_count: số lượng gợi ý tối đa
        """
        if len(suggestions) >= max_count:
            return
        
        for edge, child in node.children.items():
            new_prefix = current_prefix + edge
            
            if new_prefix.startswith(prefix):
                if child.is_end_of_word:
                    suggestions.append(new_prefix)
                collect_suggestions(child, new_prefix, suggestions, max_count)
            elif prefix.startswith(new_prefix):
                collect_suggestions(child, new_prefix, suggestions, max_count)
    
    suggestions = []
    collect_suggestions(dictionary.root, "", suggestions)
    return jsonify({"words": sorted(suggestions)[:8]})

@app.route('/api/tree')
def get_tree_structure():
    """
    API: Lấy toàn bộ cấu trúc Radix Trie dưới dạng nodes và edges cho vis.js
    Response: JSON chứa nodes và edges để vẽ graph
    """
    nodes = []
    edges = []
    node_id = [0]  # Sử dụng list để tạo closure
    
    def traverse_tree(trie_node, parent_id, prefix):
        """Duyệt cây để tạo nodes và edges"""
        for edge, child in trie_node.children.items():
            node_id[0] += 1
            current_id = node_id[0]
            new_prefix = prefix + edge
            
            # Tạo node label với edge text
            label = edge[:15] + "..." if len(edge) > 15 else edge
            color = "#4CAF50" if child.is_end_of_word else "#2196F3"
            size = 50  # Tăng từ 35/25
            
            nodes.append({
                "id": current_id,
                "label": label,
                "title": new_prefix,  # Tooltip hiển thị full text
                "color": color,
                "is_end_of_word": child.is_end_of_word,
                "is_deleted": child.is_deleted,
                "size": size
            })
            
            # Tạo edge nối từ parent
            edges.append({
                "from": parent_id,
                "to": current_id
            })
            
            # Gọi đệ quy cho các con
            traverse_tree(child, current_id, new_prefix)
    
    # Tạo root node
    nodes.append({
        "id": 0,
        "label": "ROOT",
        "color": "#FF9800",
        "size": 55  # Tăng từ 40
    })
    
    # Duyệt toàn bộ cây
    traverse_tree(dictionary.root, 0, "")
    
    return jsonify({
        "nodes": nodes,
        "edges": edges
    })

# ============================================================================
# Chạy ứng dụng
# ============================================================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
