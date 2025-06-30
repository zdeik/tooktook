// js/utils.js
// 페이지 전환 애니메이션을 위한 공통 함수
export const navigateWithFadeOut = (url) => {
    const container = document.querySelector('.container');
    if (container) {
        container.classList.add('is-leaving');
    }
    // 애니메이션 시간(0.3초) 후 페이지 이동
    setTimeout(() => {
        window.location.href = url;
    }, 300);
};