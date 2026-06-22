// chart.js
// 월간 감정 통계 그래프 시각화 모듈

async function loadEmotionChart() {
    try {
        const response = await fetch('/api/history');
        if (!response.ok) {
            console.error("서버 응답 오류:", response.status);
            return;
        }
        const historyData = await response.json(); 
        // 예: [{id:1, date:"2026-06-06", emotion:"행복/만족"}, ...]

        // 이번 달 데이터만 필터링
        const now = new Date();
        const currentMonth = now.getMonth(); // 0=1월
        const emotionCounts = {};

        historyData.forEach(entry => {
            const entryDate = new Date(entry.date);
            if (entryDate.getMonth() === currentMonth) {
                const emotion = entry.emotion;
                emotionCounts[emotion] = (emotionCounts[emotion] || 0) + 1;
            }
        });

        // Chart.js 데이터 준비
        const labels = Object.keys(emotionCounts);
        const data = Object.values(emotionCounts);

        const ctx = document.getElementById('emotionChart').getContext('2d');

        // 기존 차트가 있으면 삭제 후 새로 생성
        if (window.emotionChartInstance) {
            window.emotionChartInstance.destroy();
        }

        window.emotionChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: '이번 달 감정 횟수',
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });

    } catch (error) {
        console.error("그래프 불러오기 오류:", error);
    }
}

// 페이지 로드 시 자동 실행
window.addEventListener("load", loadEmotionChart);