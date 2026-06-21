let myChart = null; // 차트 객체를 담을 변수

// 1. 일기 분석 요청 함수 (Client-side 비동기 처리)
async function analyzeEmotion() {
    const sentence = document.getElementById("diary-input").value.trim();
    
    if (!sentence) {
        alert("내용을 입력해 주세요!");
        return;
    }

    // 로딩창 켜고 결과창 숨기기
    document.getElementById("loading").style.display = "block";
    document.getElementById("result-section").style.display = "none";

    try {
        // FastAPI 서버의 /api/analyze 엔드포인트로 데이터 전송
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sentence: sentence })
        });

        const data = await response.json();

        // 화면에 결과 반영
        document.getElementById("emotion-result").innerText = data.emotion;
        document.getElementById("quote-result").innerText = data.message;
        
        document.getElementById("result-section").style.display = "block";
        
        // 분석이 끝나면 그래프도 자동으로 갱신
        loadEmotionChart();

    } catch (error) {
        alert("서버 통신 중 오류가 발생했습니다.");
        console.error(error);
    } finally {
        // 로딩창 숨기기
        document.getElementById("loading").style.display = "none";
    }
}

// 2. DB에서 데이터를 받아와 차트를 그리는 함수
async function loadEmotionChart() {
    try {
        // 저장된 전체 감정 데이터 가져오기
        // main.js 내부 수정
        const response = await fetch('/api/history');
        const history = await response.json(); // [{id:1, date:..., emotion:...}, ...]

        // 감정별 빈도수 계산을 위한 바구니
        const counts = {
            "행복/만족": 0, "우울/피곤": 0, "불안/걱정": 0, 
            "분노/짜증": 0, "설렘/흥분": 0, "외로움/공허": 0, "평온/안정": 0
        };

        // 데이터 개수 세기
        history.forEach(item => {
            if (counts[item.emotion] !== undefined) {
                counts[item.emotion]++;
            }
        });

        // Chart.js에 들어갈 데이터 배열 생성
        const labels = Object.keys(counts);
        const chartData = Object.values(counts);

        // 기존에 그려진 차트가 있다면 파괴하고 새로 생성 (중복 생성 방지)
        if (myChart) { myChart.destroy(); }

        const ctx = document.getElementById('emotionChart').getContext('2d');
        myChart = new Chart(ctx, {
            type: 'pie', // 원형 그래프
            data: {
                labels: labels,
                datasets: [{
                    data: chartData,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', 
                        '#FF9F40', '#9966FF', '#C9CBCF', '#4BC0C0'
                    ]
                }]
            },
            options: {
                responsive: true
            }
        });

    } catch (error) {
        console.error("차트를 불러오는 중 오류 발생:", error);
    }
}

// 페이지가 처음 켜질 때도 자동으로 그래프를 그려줌
window.onload = loadEmotionChart;