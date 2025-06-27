// js/memo.js
// 상담가 메모 관련 기능 초기화 함수
export function initMemo() {
    const memoTextArea = document.getElementById('memoTextArea');
    const saveMemoBtn = document.getElementById('saveMemoBtn');

    // 메모장 관련 요소가 없는 페이지라면 아무것도 하지 않음
    if (!memoTextArea || !saveMemoBtn) return;

    const loadMemo = () => {
        const savedMemo = localStorage.getItem('counselorMemo');
        if (savedMemo) {
            memoTextArea.value = savedMemo;
        }
    };

    const saveMemo = () => {
        localStorage.setItem('counselorMemo', memoTextArea.value);
        
        const originalText = saveMemoBtn.textContent;
        saveMemoBtn.textContent = '저장됨!';
        saveMemoBtn.disabled = true;
        setTimeout(() => {
            saveMemoBtn.textContent = originalText;
            saveMemoBtn.disabled = false;
        }, 1500);
    };

    saveMemoBtn.addEventListener('click', saveMemo);
    
    // 페이지 로드 시 저장된 메모 불러오기
    loadMemo();
}