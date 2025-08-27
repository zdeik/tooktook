// js/swipeToggle.js
import { navigateWithFadeOut } from './utils.js';

// ON/OFF 스와이프 토글 기능 초기화 함수
export function initSwipeToggle() {
    const swipeToggle = document.getElementById('swipeToggle');
    if (!swipeToggle) return;
    
    const knob = swipeToggle.querySelector('.swipe-knob');
    const toggleText = swipeToggle.querySelector('.toggle-text');
    let isDragging = false;
    let startX = 0;

    const activateOnState = () => {
        if (swipeToggle.classList.contains('on')) return;
        swipeToggle.classList.replace('off', 'on');
        swipeToggle.setAttribute('aria-checked', 'true');
        toggleText.textContent = 'ON';
        sessionStorage.setItem('consultationStartTime', new Date().getTime());
        setTimeout(() => { navigateWithFadeOut('consultation.html'); }, 400);
    };

    const deactivateOffState = () => {
        if (swipeToggle.classList.contains('off')) return;
        swipeToggle.classList.replace('on', 'off');
        swipeToggle.setAttribute('aria-checked', 'false');
        toggleText.textContent = 'OFF';
    };

    swipeToggle.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); if (swipeToggle.classList.contains('off')) activateOnState(); else deactivateOffState(); }
    });
    
    const snapToPosition = () => {
        const currentLeft = parseInt(knob.style.left || '4px');
        const threshold = swipeToggle.offsetWidth / 2;
        if (swipeToggle.classList.contains('off')) {
            if (currentLeft > threshold - (knob.offsetWidth / 2)) activateOnState(); else knob.style.left = '4px';
        } else {
            if (currentLeft < threshold - (knob.offsetWidth / 2)) deactivateOffState(); else knob.style.left = '82px';
        }
    };
    
    const dragStart = (e) => {
        e.preventDefault(); isDragging = true; startX = e.type === 'touchstart' ? e.touches[0].clientX : e.clientX; knob.style.transition = 'none';
    };
    
    const dragMove = (e) => {
        if (!isDragging) return;
        const currentX = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX;
        let moveX = currentX - startX;
        const minLeft = 4, maxLeft = 82;
        let newLeft = (swipeToggle.classList.contains('on') ? maxLeft : minLeft) + moveX;
        if (newLeft < minLeft) newLeft = minLeft; if (newLeft > maxLeft) newLeft = maxLeft;
        knob.style.left = `${newLeft}px`;
    };
    
    const dragEnd = () => {
        if (!isDragging) return; isDragging = false; knob.style.transition = 'left 0.3s ease'; snapToPosition();
    };
    
    swipeToggle.addEventListener('mousedown', dragStart);
    swipeToggle.addEventListener('touchstart', dragStart, { passive: false });
    window.addEventListener('mousemove', dragMove);
    window.addEventListener('touchmove', dragMove);
    window.addEventListener('mouseup', dragEnd);
    window.addEventListener('touchend', dragEnd);
    
    swipeToggle.addEventListener('click', (e) => {
        if (Math.abs(e.clientX - startX) > 5) return; if (swipeToggle.classList.contains('off')) activateOnState(); else deactivateOffState();
    });
}