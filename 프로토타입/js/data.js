// js/data.js
// 상담 이력 가상 데이터
export const mockHistoryData = [
    { 
        id: 1, clientName: '김민준', summary: '대출 조건 관련 문의', date: '2025-06-27',
        chatLog: [
            { speaker: 'counselor', text: '안녕하세요 상담사 톡톡입니다. 무엇을 도와드릴까요?' },
            { speaker: 'user', text: '안녕하세요. 대출 조건이 어떻게 되는지 궁금해서요.' },
            { speaker: 'counselor', text: '네, 고객님. 소득 증빙과 신용 등급에 따라 조건이 달라질 수 있습니다. 자세한 안내를 도와드리겠습니다.' }
        ]
    },
    { 
        id: 2, clientName: '이서연', summary: '서류 발급 절차 문의', date: '2025-06-27',
        chatLog: [
            { speaker: 'user', text: '필요한 서류를 어디서 발급받아야 하나요?' },
            { speaker: 'counselor', text: '주민등록등본은 정부24, 소득증빙서류는 국세청 홈택스에서 발급 가능합니다.' }
        ]
    },
    { id: 3, clientName: '박도윤', summary: '앱 사용법 문의', date: '2025-06-26', chatLog: [] },

    
];

// [추가] 상담사 ID 및 이름 데이터
export const mockCounselors = [
    { id: '40', name: '박상준' },
    { id: '21', name: '한지훈' },
    { id: '51', name: '홍가연' },
    { id: '72', name: '이정석' }
];
