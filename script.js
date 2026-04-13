// ============================================================================
// English Dictionary Web Application - Frontend Logic
// ============================================================================

// DOM Element References
const inpWord = document.getElementById('inp-word');
const searchBtn = document.getElementById('search-btn');
const result = document.getElementById('result');
const suggestionsList = document.getElementById('suggestions-list');
const treeCanvas = document.getElementById('tree-canvas');

// HTML Template References untuk dynamic content generation
const wordResultTemplate = document.getElementById('word-result-template');
const addFormTemplate = document.getElementById('add-form-template');

// ============================================================================
// Tree Visualization - vis.js Network
// ============================================================================

let treeNetwork = null;

/**
 * Vẽ tree visualization bằng vis.js Network
 */
async function updateTreeVisualization() {
    try {
        const response = await fetch('/api/tree');
        const treeData = await response.json();
        const searchKeyword = inpWord.value.trim().toLowerCase();
        drawTreeVis(treeData.nodes, treeData.edges, searchKeyword);
    } catch (error) {
        console.error('Error updating tree:', error);
    }
}

/**
 * Vẽ tree bằng vis.js Network
 */
function drawTreeVis(nodes, edges, searchKeyword = '') {
    // Color palette - mau toi de nhin tren nen trang (tránh trùng đỏ #FF0000 và vàng #FFD700)
    const colorPalette = [
        '#FF9800',  
        '#2196F3',  
        '#4CAF50',  
        '#c26a19',  
        '#02aa10',
        '#E67E9E',  
        '#07c5ff',
        '#9B59B6', 
        '#2C3E50',  
        '#a80773'
    ];
    
    // Tính depth của mỗi node bằng BFS
    const nodeDepths = {};
    
    // Khởi tạo depth cho tất cả nodes
    nodes.forEach(n => {
        nodeDepths[n.id] = 0;
    });
    
    // BFS từ root nodes
    const rootNodes = nodes.filter(n => !edges.some(e => e.to === n.id));
    const queue = rootNodes.map(n => ({id: n.id, depth: 0}));
    
    while (queue.length > 0) {
        const {id, depth} = queue.shift();
        nodeDepths[id] = Math.max(nodeDepths[id], depth);
        
        const childEdges = edges.filter(e => e.from === id);
        childEdges.forEach(e => {
            queue.push({id: e.to, depth: depth + 1});
        });
    }
    
    // Đảm bảo tất cả nodes có depth (fallback cho orphan nodes)
    nodes.forEach(n => {
        if (nodeDepths[n.id] === undefined) {
            nodeDepths[n.id] = 0;
        }
    });
    
    // Transform data for vis.js
    const visNodes = new vis.DataSet(nodes.map(n => ({
        id: n.id,
        label: n.label || n.id,
        // Vàng nếu node là từ complete (is_end_of_word=true) và khớp exact với keyword, đỏ nếu deleted, còn lại dùng palette theo depth
        color: (searchKeyword && n.is_end_of_word && n.title && n.title.toLowerCase() === searchKeyword) ? '#FFD700' : 
               (n.is_deleted ? '#FF0000' : colorPalette[nodeDepths[n.id] % colorPalette.length]),
        title: n.label || n.id,
        shape: 'circle',
        font: { size: 14, color: '#fff', bold: { color: '#fff' } },
        borderWidth: 2,
        borderWidthSelected: 3,
        fixed: false  // Di chuyển tự do
    })));
    
    
    const visEdges = new vis.DataSet(edges.map(e => {
        // Lấy màu từ node nguồn (parent)
        const sourceNodeColor = colorPalette[nodeDepths[e.from] % colorPalette.length];
        return {
            from: e.from,
            to: e.to,
            arrows: 'to',
            color: sourceNodeColor,
            smooth: { 
                type: 'cubicBezier',
                forceDirection: 'vertical'
            },
            width: 3
        };
    }));
    
    const data = { nodes: visNodes, edges: visEdges };
    
    // Cấu hình vis.js
    const options = {
        physics: {
            enabled: false,  // Tắt physics hoàn toàn
            stabilization: { iterations: 0 }
        },
        layout: {
            randomSeed: 42,
            hierarchical: {
                enabled: false  // Disable hierarchical để cho phép drag tự do
            }
        },
        interaction: {
            zoomView: true,  // Cho phép zoom
            dragView: true,  // Cho phép drag canvas
            dragNodes: true, // Cho phép drag nodes
            hover: false,
            navigationButtons: false,
            keyboard: false
        },
        nodes: {
            shape: 'circle',
            margin: 10,
            widthConstraint: { maximum: 200 },
            font: { size: 14, color: '#333' }
        }
    };
    
    if (treeNetwork === null) {
        treeNetwork = new vis.Network(treeCanvas, data, options);
        
        // Sau khi load, fit view
        setTimeout(() => {
            treeNetwork.fit();
            treeNetwork.stopSimulation();
        }, 500);
    } else {
        treeNetwork.setData(data);
        treeNetwork.setOptions(options);
        treeNetwork.stopSimulation();
        
        setTimeout(() => {
            treeNetwork.fit();
            treeNetwork.stopSimulation();
        }, 300);
    }
}

// Cập nhật tree khi page load
document.addEventListener('DOMContentLoaded', updateTreeVisualization);

// ============================================================================
// Event Listeners - Xử lý các sự kiện từ người dùng
// ============================================================================

// Xử lý click vào nút "Search"
searchBtn.addEventListener('click', searchWord);

// Xử lý phím Enter để tìm kiếm
inpWord.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchWord();
});

// Xử lý input để hiển thị gợi ý khi người dùng gõ
inpWord.addEventListener('input', showSuggestions);

// ============================================================================
// GỢI Ý - Suggestions
// ============================================================================

/**
 * Hiển thị danh sách gợi ý từ khi người dùng gõ tiền tố
 */
async function showSuggestions() {
    const prefix = inpWord.value.trim().toLowerCase();
    
    // Ẩn gợi ý nếu input trống
    if (!prefix || prefix.length < 1) {
        suggestionsList.classList.remove('show');
        return;
    }
    
    try {
        // Gọi API để lấy gợi ý từ dựa trên tiền tố
        const response = await fetch(`/api/suggestions?prefix=${encodeURIComponent(prefix)}`);
        const data = await response.json();
        
        // Hiển thị gợi ý nếu có kết quả
        if (data.words && data.words.length > 0) {
            suggestionsList.innerHTML = data.words
                .map(word => `<div class="suggestion-item" onclick="selectSuggestion('${word}')">${word}</div>`)
                .join('');
            suggestionsList.classList.add('show');
        } else {
            suggestionsList.classList.remove('show');
        }
    } catch (error) {
        suggestionsList.classList.remove('show');
    }
}

/**
 * Xử lý khi người dùng chọn một gợi ý từ danh sách
 * @param {string} word - Từ được chọn
 */
function selectSuggestion(word) {
    inpWord.value = word;
    suggestionsList.classList.remove('show');
    searchWord();
}

// ============================================================================
// TÌM KIẾM - Search
// ============================================================================

/**
 * Tìm kiếm từ trong từ điển và hiển thị kết quả
 */
async function searchWord() {
    const word = inpWord.value.trim();
    
    // Kiểm tra input không trống
    if (!word) {
        alert('Vui lòng nhập một từ để tìm kiếm....');
        return;
    }
    
    // Ẩn gợi ý khi tìm kiếm
    suggestionsList.classList.remove('show');
    
    try {
        // Gọi API tìm kiếm
        const response = await fetch(`/api/search?word=${encodeURIComponent(word)}`);
        const data = await response.json();
        
        if (response.ok) {
            displayResult(data);
            updateTreeVisualization(); // Cập nhật tree khi tìm kiếm
        } else {
            alert(data.error || 'Từ không tìm thấy ❌');
        }
    } catch (error) {
        alert('Lỗi khi lấy dữ liệu ❌');
    }
}

/**
 * Hiển thị kết quả tìm kiếm (định nghĩa, ví dụ, cách phát âm)
 * @param {object} data - Dữ liệu từ từ API
 */
function displayResult(data) {
    // Clone HTML template để tạo UI động
    const wordDiv = wordResultTemplate.content.cloneNode(true);
    
    // Hiển thị từ được tìm kiếm
    wordDiv.getElementById('result-word').textContent = data.word;
    
    // Hiển thị định nghĩa
    wordDiv.getElementById('result-definition').textContent = data.definition;
    
    // Hiển thị cách phát âm (nếu có)
    const pronunciationEl = wordDiv.getElementById('result-pronunciation');
    if (data.pronunciation) {
        pronunciationEl.textContent = data.pronunciation;
    } else {
        pronunciationEl.style.display = 'none';
    }
    
    // Hiển thị danh sách ví dụ
    const examplesContainer = wordDiv.getElementById('result-examples');
    const examplesHTML = data.examples && data.examples.length > 0
        ? data.examples.map(ex => `<div class="example">${ex}</div>`).join('')
        : '';
    examplesContainer.innerHTML = examplesHTML;
    
    // Gán hàm xóa từ cho nút Delete
    const deleteBtn = wordDiv.getElementById('result-delete-btn');
    deleteBtn.onclick = () => deleteWord(data.word);
    
    // Xóa kết quả cũ và thêm kết quả mới vào DOM
    result.innerHTML = '';
    result.appendChild(wordDiv);
}

// ============================================================================
// XÓA TỪ - Delete Word
// ============================================================================

/**
 * Xóa một từ khỏi từ điển
 * @param {string} word - Từ cần xóa
 */
async function deleteWord(word) {
    // Xin xác nhận từ người dùng
    if (!confirm(`Bạn có chắc chắn muốn xóa từ "${word}"?`)) return;
    
    try {
        // Gọi API xóa từ
        const response = await fetch('/api/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ word })
        });
        
        if (response.ok) {
            alert(`Xóa "${word}" thành công ✅`);
            inpWord.value = '';
            updateTreeVisualization(); // Cập nhật tree khi xóa từ
        } else {
            const data = await response.json();
            alert(data.error);
        }
    } catch (error) {
        alert('Lỗi khi xóa từ ❌');
    }
}

// ============================================================================
// THÊM TỪ - Add Word
// ============================================================================

/**
 * Hiển thị form để thêm từ mới
 */
function showAddForm() {
    // Xóa form cũ nếu có
    const oldForm = document.querySelector('.add-form-wrapper');
    if (oldForm) {
        oldForm.remove();
    }
    
    // Clone add form template
    const formDiv = addFormTemplate.content.cloneNode(true);
    
    // Thêm form vào kết quả
    result.appendChild(formDiv);
}

/**
 * Hủy form thêm từ
 */
function cancelAddForm() {
    // Tìm và xóa form wrapper từ DOM
    const formDiv = document.querySelector('.add-form-wrapper');
    if (formDiv) {
        formDiv.remove();
    }
}

/**
 * Gửi từ mới tới server để thêm vào từ điển
 */
async function submitNewWord() {
    // Lấy dữ liệu từ form
    const word = document.getElementById('new-word').value.trim().toLowerCase();
    const definition = document.getElementById('new-definition').value.trim();
    const pronunciation = document.getElementById('new-pronunciation').value.trim();
    const examplesStr = document.getElementById('new-examples').value.trim();
    
    // Kiểm tra dữ liệu bắt buộc
    if (!word || !definition) {
        alert('Vui lòng nhập từ và định nghĩa');
        return;
    }
    
    // Xử lý ví dụ - split bằng dấu chấm phẩy
    const examples = examplesStr ? examplesStr.split(';').map(e => e.trim()) : [];
    
    try {
        // Gọi API thêm từ
        const response = await fetch('/api/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ word, definition, pronunciation, examples })
        });
        
        if (response.ok) {
            alert('✓ Từ được thêm thành công!');
            inpWord.value = word;
            updateTreeVisualization(); // Cập nhật tree khi thêm từ mới
            searchWord(); // Hiển thị từ vừa thêm
        } else {
            const data = await response.json();
            // Kiểm tra nếu từ đã tồn tại
            if (response.status === 409) {
                alert(`Từ "${word}" đã tồn tại. Vui lòng thêm từ khác hoặc xóa từ.`);
            } else {
                alert(data.error);
            }
        }
    } catch (error) {
        alert('Lỗi khi thêm từ');
    }
}

