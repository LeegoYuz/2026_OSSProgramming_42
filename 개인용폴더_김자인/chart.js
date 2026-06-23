// 차트 객체를 전역 변수로 선언 (중복 생성 방지용)
let pieChartInstance = null;
let barChartInstance = null;

async function loadDashboardCharts() {
    try {
        // FastAPI 서버에 과거 일기 기록 요청
        const response = await fetch('http://127.0.0.1:8000/api/history');
        const history = await response.json();

        // CONSTANTS.py의 EMOTIONS_LIST 구조와 동일하게 바구니 세팅
        const counts = {
            "행복/만족": 0, "우울/피곤": 0, "불안/걱정": 0, 
            "분노/짜증": 0, "설렘/흥분": 0, "외로움/공허": 0, "평온/안정": 0
        };

        // 데이터 개수 카운트
        history.forEach(item => {
            if (counts[item.emotion] !== undefined) {
                counts[item.emotion]++;
            }
        });

        const labels = Object.keys(counts);
        const chartData = Object.values(counts);

        // 공통으로 사용할 예쁜 파스텔톤 테마 색상
        const colors = [
            '#FF6384', '#36A2EB', '#FFCE56', 
            '#FF9F40', '#9966FF', '#C9CBCF', '#4BC0C0'
        ];

        // 1. 원형 차트 (Pie Chart) 그리기
        if (pieChartInstance) { pieChartInstance.destroy(); }
        const ctxPie = document.getElementById('emotionPieChart').getContext('2d');
        pieChartInstance = new Chart(ctxPie, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: chartData,
                    backgroundColor: colors
                }]
            },
            options: { responsive: true }
        });

        // 2. 막대 차트 (Bar Chart) 그리기
        if (barChartInstance) { barChartInstance.destroy(); }
        const ctxBar = document.getElementById('emotionBarChart').getContext('2d');
        barChartInstance = new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: '기록 횟수 (일)',
                    data: chartData,
                    backgroundColor: colors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 } // 정수 형태로만 표현되도록 설정
                    }
                }
            }
        });

    } catch (error) {
        console.error("대시보드 차트를 불러오는 중 오류 발생:", error);
    }
}

// 대시보드 페이지가 로드되면 자동으로 실행
window.onload = loadDashboardCharts;