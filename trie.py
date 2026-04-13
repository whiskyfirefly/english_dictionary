class RadixTrieNode:
    """Nút trong cây Radix Trie"""
    def __init__(self):
        # Dictionary lưu các cạnh (edge) nối tới các nút con
        self.children = {}
        # Flag đánh dấu nút là kết thúc một từ hoàn chỉnh
        self.is_end_of_word = False
        # Flag đánh dấu nút bị xóa (từng là end_of_word nhưng bây giờ không)
        self.is_deleted = False
        # Dữ liệu từ: định nghĩa, ví dụ, phát âm
        self.word_data = None


class RadixTrie:
    """Cây Radix Trie - cấu trúc dữ liệu tối ưu cho từ điển"""
    
    def __init__(self):
        # Nút gốc của cây
        self.root = RadixTrieNode()

    def _common_prefix_len(self, s1, s2):
        """
        Tính độ dài tiền tố chung của hai chuỗi
        - s1: chuỗi thứ nhất
        - s2: chuỗi thứ hai
        - Return: độ dài tiền tố chung
        """
        i = 0
        while i < min(len(s1), len(s2)) and s1[i] == s2[i]:
            i += 1
        return i

    def insert(self, word, definition=None, examples=None, pronunciation=None):
        """
        Thêm từ vào trie với thông tin đi kèm
        - word: từ cần thêm
        - definition: định nghĩa
        - examples: danh sách ví dụ
        - pronunciation: cách phát âm
        """
        node = self.root
        while word:
            for edge, child in node.children.items():
                common = self._common_prefix_len(word, edge)
                if common == 0:
                    continue

                # Edge khớp hoàn toàn - tiếp tục đi sâu
                if common == len(edge):
                    node = child
                    word = word[common:]
                    break
                # Cần tách edge - tạo nút mới
                else:
                    new_node = RadixTrieNode()
                    new_node.children[edge[common:]] = child
                    node.children[word[:common]] = new_node
                    del node.children[edge]

                    # Thêm phần còn lại của từ
                    if common < len(word):
                        tail = RadixTrieNode()
                        tail.is_end_of_word = True
                        tail.is_deleted = False
                        tail.word_data = {"definition": definition, "examples": examples, "pronunciation": pronunciation}
                        new_node.children[word[common:]] = tail
                    else:
                        new_node.is_end_of_word = True
                        new_node.is_deleted = False
                        new_node.word_data = {"definition": definition, "examples": examples, "pronunciation": pronunciation}
                    return
            else:
                # Không tìm thấy edge khớp - thêm cạnh mới
                new_node = RadixTrieNode()
                new_node.is_end_of_word = True
                new_node.is_deleted = False
                new_node.word_data = {"definition": definition, "examples": examples, "pronunciation": pronunciation}
                node.children[word] = new_node
                return
        
        # Khi word trở thành trống - node hiện tại là node terminal
        # Nếu node này từng bị xóa, cập nhật lại is_deleted và word_data
        node.is_end_of_word = True
        node.is_deleted = False
        node.word_data = {"definition": definition, "examples": examples, "pronunciation": pronunciation}

    def _traverse(self, text):
        """
        Duyệt cây để tìm nút kết thúc với text cho trước
        - text: chuỗi tìm kiếm
        - Return: nút tương ứng hoặc None
        """
        node = self.root
        while text:
            for edge, child in node.children.items():
                if text.startswith(edge):
                    text = text[len(edge):]
                    node = child
                    break
                elif edge.startswith(text):
                    return node
            else:
                return None
        return node

    def search(self, word):
        """
        Kiểm tra từ có tồn tại trong từ điển
        - word: từ cần tìm
        - Return: True nếu tìm thấy, False nếu không
        """
        node = self._traverse(word)
        return node is not None and node.is_end_of_word

    def get_definition(self, word):
        """
        Lấy thông tin định nghĩa của một từ
        - word: từ cần tra cứu
        - Return: từ điển chứa definition, examples, pronunciation hoặc None
        """
        node = self._traverse(word)
        if node is None or not node.is_end_of_word:
            return None
        return node.word_data

    def starts_with(self, prefix):
        """
        Kiểm tra có từ nào bắt đầu với tiền tố cho trước
        - prefix: tiền tố cần kiểm tra
        - Return: True nếu có, False nếu không
        """
        return self._traverse(prefix) is not None

    def delete(self, word):
        """
        Xóa một từ khỏi từ điển
        - word: từ cần xóa
        - Return: True nếu xóa thành công, False nếu không tìm thấy
        """
        node = self._traverse(word)
        if node is None or not node.is_end_of_word:
            return False
        node.is_end_of_word = False
        node.is_deleted = True
        node.word_data = None
        return True
