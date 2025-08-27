import { navigateWithFadeOut } from './utils.js';
import { mockCounselors } from './data.js';
import { initHistory } from './history.js';
import { initMemo } from './memo.js';
import { initSwipeToggle } from './swipeToggle.js';

// DOM이 로드되면 애플리케이션 초기화 시작
document.addEventListener('DOMContentLoaded', () => {

    /* =============================================
       1. 공통 로직 실행 (모든 페이지에서 실행)
       ============================================= */

    // --- 공통: 현재 날짜 표시 ---
    const dateDisplayElement = document.getElementById('currentDate');
    if (dateDisplayElement) {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        dateDisplayElement.textContent = `날짜 ${year}/${month}/${day}`;
    }

    // --- [추가된 코드] 공통: 로그인된 상담사 이름 표시 ---
    const counselorNameDisplay = document.getElementById('counselorNameDisplay');
    if (counselorNameDisplay) {
        const counselorData = sessionStorage.getItem('loggedInCounselor');
        if (counselorData) {
            const counselor = JSON.parse(counselorData);
            counselorNameDisplay.textContent = `상담가: ${counselor.name}`;
        }
    }


    /* =============================================
       2. 페이지별 이벤트 리스너 및 기능 초기화
       ============================================= */

    // --- 로그인 페이지 로직 ---
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', () => {
            const counselorIdInput = document.getElementById('counselorId');
            const errorMessage = document.getElementById('errorMessage');
            const enteredId = counselorIdInput.value.trim();

            if (enteredId === '') {
                errorMessage.textContent = '상담사 번호를 입력해주세요.';
                errorMessage.style.visibility = 'visible';
                return;
            }
            
            const counselor = mockCounselors.find(c => c.id === enteredId);

            if (counselor) {
                errorMessage.style.visibility = 'hidden';
                sessionStorage.setItem('loggedInCounselor', JSON.stringify(counselor));
                
                loginBtn.disabled = true;
                loginBtn.classList.add('loading');
                setTimeout(() => { navigateWithFadeOut('waiting.html'); }, 1000);
            } else {
                errorMessage.textContent = '존재하지 않는 상담사 번호입니다.';
                errorMessage.style.visibility = 'visible';
            }
        });
    }

    // --- 상담 페이지 로직 (타이머 제외) ---
    const endBtn = document.getElementById('endBtn');
    if (endBtn) {
        endBtn.addEventListener('click', () => { navigateWithFadeOut('waiting.html'); });
    }

    // --- 대기 페이지: 드롭다운 메뉴 로직 ---
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userMenu = document.getElementById('userMenu');
    if (userMenuBtn && userMenu) {
        userMenuBtn.addEventListener('click', () => {
            const isHidden = userMenu.classList.toggle('is-hidden');
            userMenuBtn.setAttribute('aria-expanded', !isHidden);
        });

        window.addEventListener('click', (e) => {
            if (!userMenuBtn.contains(e.target) && !userMenu.contains(e.target)) {
                userMenu.classList.add('is-hidden');
                userMenuBtn.setAttribute('aria-expanded', 'false');
            }
        });

        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !userMenu.classList.contains('is-hidden')) {
                userMenu.classList.add('is-hidden');
                userMenuBtn.setAttribute('aria-expanded', 'false');
                userMenuBtn.focus();
            }
        });

        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                // 실제 앱에서는 sessionStorage.removeItem('loggedInCounselor') 등
                // 로그인 정보를 지우는 처리도 추가됩니다.
                console.log('로그아웃 되었습니다.');
                navigateWithFadeOut('index.html');
            });
        }
    }


    /* =============================================
       3. 모듈화된 기능 초기화
       ============================================= */
    initHistory();
    initMemo();
    initSwipeToggle();
    // initConsultationTimer(); // 타이머 기능은 취소되었으므로 호출하지 않음
});