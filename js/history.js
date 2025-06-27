import { navigateWithFadeOut } from './utils.js';
import { mockHistoryData } from './data.js';

// 이 모듈의 모든 기능을 초기화하고 이벤트 리스너를 등록하는 메인 함수
export function initHistory() {
    // 현재 페이지에 따라 적절한 기능 실행
    if (document.body.dataset.page === 'history-detail') {
        handleHistoryDetailPage();
    } else if (document.querySelector('.history-list')) {
        handleWaitingPage();
    }
}

// --- 페이지별 로직을 처리하는 함수들 ---

/**
 * 대기 페이지의 모든 기능(목록 렌더링, 검색, 모달)을 처리하는 함수
 */
function handleWaitingPage() {
    // 1. 필요한 모든 DOM 요소 가져오기
    const historySection = document.querySelector('.history-section');
    const historyList = document.querySelector('.history-list');
    const searchInput = document.getElementById('searchInput');
    const template = document.getElementById('history-item-template');
    
    // 모달 관련 요소
    const modalOverlay = document.querySelector('.modal-overlay');
    const modal = modalOverlay.querySelector('.modal');
    const modalContent = modalOverlay.querySelector('.modal-content');
    const modalCloseBtn = modalOverlay.querySelector('.modal-close-btn');
    let lastFocusedElement; // 모달 닫기 후 포커스를 돌려줄 요소

    // 2. 핵심 기능 함수 정의
    
    // 모달을 여는 함수
    const openModal = (item) => {
        lastFocusedElement = document.activeElement;
        modalContent.innerHTML = `
            <div class="memo-detail">
                <h3>${item.clientName}님 상담 요약</h3>
                <p><strong>상담 일자:</strong> ${item.date}</p>
                <p><strong>상담 내용:</strong> ${item.summary}</p>
                <p style="text-align: center; margin-top: 20px; color: #888;">(상세 내용을 보려면 이 창을 클릭하세요)</p>
            </div>
        `;
        modal.dataset.historyId = item.id;
        modalOverlay.classList.remove('is-hidden');
        modalCloseBtn.focus();
    };

    // 모달을 닫는 함수
    const closeModal = () => {
        modalOverlay.classList.add('is-hidden');
        if (lastFocusedElement) lastFocusedElement.focus();
    };

    // 상담 이력 목록을 그리는 함수
    const renderHistoryList = (historyData, emptyMessage = "상담 이력이 없습니다.") => {
        if (!historyList || !template) return;
        historyList.innerHTML = '';
        if (historyData.length === 0) {
            historySection.classList.add('is-empty');
            const emptyStateText = historySection.querySelector('.empty-state p');
            if (emptyStateText) emptyStateText.textContent = emptyMessage;
        } else {
            historySection.classList.remove('is-empty');
            historyData.forEach(item => {
                const itemNode = document.importNode(template.content, true);
                const listItem = itemNode.querySelector('.history-list-item');
                listItem.dataset.id = item.id;
                listItem.querySelector('.history-client').textContent = item.clientName;
                listItem.querySelector('.history-summary').textContent = item.summary;
                historyList.appendChild(itemNode);
            });
        }
    };

    // 3. 이벤트 리스너 등록
    
    // 검색창 입력 이벤트
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            const filteredData = mockHistoryData.filter(item => 
                item.clientName.toLowerCase().includes(searchTerm)
            );
            renderHistoryList(filteredData, "검색 결과가 없습니다.");
        });
    }

    // 목록 아이템 클릭 이벤트 (이벤트 위임)
    historyList.addEventListener('click', (e) => {
        const clickedItem = e.target.closest('.history-list-item');
        if (!clickedItem) return;
        const clickedId = parseInt(clickedItem.dataset.id, 10);
        const selectedData = mockHistoryData.find(item => item.id === clickedId);
        if (selectedData) openModal(selectedData);
    });
    
    // 모달 클릭 시 상세 페이지로 이동
    if (modal) {
        modal.addEventListener('click', () => {
            const historyId = modal.dataset.historyId;
            if(historyId) navigateWithFadeOut(`history-detail.html?id=${historyId}`);
        });
    }

    // 모달 닫기 이벤트들
    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            closeModal();
        });
    }
    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) closeModal();
        });
    }
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !modalOverlay.classList.contains('is-hidden')) {
            closeModal();
        }
    });

    // 4. 초기 실행
    renderHistoryList(mockHistoryData);
}

/**
 * 상담 이력 상세 페이지의 모든 기능을 처리하는 함수
 */
function handleHistoryDetailPage() {
    const urlParams = new URLSearchParams(window.location.search);
    const historyId = parseInt(urlParams.get('id'), 10);
    const historyData = mockHistoryData.find(item => item.id === historyId);

    if (historyData) {
        const counselorData = sessionStorage.getItem('loggedInCounselor');
        const counselorName = counselorData ? JSON.parse(counselorData).name : '상담사';

        document.getElementById('historyClientName').textContent = `상담자: ${historyData.clientName}`;
        document.getElementById('historyDate').textContent = `상담일: ${historyData.date}`;
        document.getElementById('historySummaryPanel').innerHTML = `<p><strong>상담 요약:</strong> ${historyData.summary}</p>`;
        
        const chatLogPanel = document.querySelector('.chat-log-panel');
        const template = document.getElementById('chat-log-item-template');
        
        if (chatLogPanel && template && historyData.chatLog.length > 0) {
            chatLogPanel.innerHTML = '';
            historyData.chatLog.forEach(log => {
                const itemNode = document.importNode(template.content, true);
                const bubble = itemNode.querySelector('.chat-bubble');
                bubble.classList.add(log.speaker);
                itemNode.querySelector('.speaker').textContent = log.speaker === 'user' ? historyData.clientName : counselorName;
                itemNode.querySelector('.message').textContent = log.text;
                chatLogPanel.appendChild(itemNode);
            });
        } else if(chatLogPanel) {
            chatLogPanel.innerHTML = '<p>저장된 대화 로그가 없습니다.</p>';
        }
    }
    
    const backToListBtn = document.getElementById('backToListBtn');
    if(backToListBtn) {
       backToListBtn.addEventListener('click', () => { navigateWithFadeOut('waiting.html'); });
    }
}