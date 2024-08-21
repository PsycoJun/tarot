// 주어진 요소의 중앙 좌표를 계산하는 함수
function getElementCenter(el) {
    const rect = el.getBoundingClientRect();
    return {
        x: rect.left + rect.width / 2,
        y: rect.top + rect.height / 2
    };
}

// 두 좌표 간의 거리 계산 함수
function distance(p1, p2) {
    return Math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2);
}

// 삼각형인지 확인하는 함수
function isTriangle(points, tolerance) {
    if (points.length !== 3) return false;

    const [p1, p2, p3] = points;
    const d1 = distance(p1, p2);
    const d2 = distance(p2, p3);
    const d3 = distance(p3, p1);

    // 평균 거리를 기준으로 허용 오차를 설정합니다.
    const avg = (d1 + d2 + d3) / 3;
    const toleranceRange = avg * tolerance;

    return (
        Math.abs(d1 - d2) <= toleranceRange &&
        Math.abs(d2 - d3) <= toleranceRange &&
        Math.abs(d3 - d1) <= toleranceRange
    );
}

// 십자가인지 확인하는 함수
function isCross(points, tolerance) {
    if (points.length !== 5) return false;

    const center = points[2];
    const top = points[0];
    const bottom = points[4];
    const left = points[1];
    const right = points[3];

    const dTop = distance(center, top);
    const dBottom = distance(center, bottom);
    const dLeft = distance(center, left);
    const dRight = distance(center, right);

    const toleranceRange = tolerance;

    const isVerticalSymmetry = Math.abs(dTop - dBottom) <= toleranceRange;
    const isHorizontalSymmetry = Math.abs(dLeft - dRight) <= toleranceRange;

    return isVerticalSymmetry && isHorizontalSymmetry;
}


// 버튼 좌표를 기준으로 상, 좌, 중, 우, 하를 판별하는 함수
function determineOrder(points) {
    if (points.length !== 5) return [];

    let top = points[0];
    let left = points[0];
    let centerPoint = points[0];
    let right = points[0];
    let bottom = points[0];

    // 상, 하를 먼저 판별
    points.forEach(point => {
        if (point.y < top.y) {
            top = point;
        }
        if (point.y > bottom.y) {
            bottom = point;
        }
    });

    // 좌, 우를 판별
    points.forEach(point => {
        if (point !== top && point !== bottom) {
            if (point.x < left.x) {
                left = point;
            }
            if (point.x > right.x) {
                right = point;
            }
        }
    });

    // 나머지 점은 중앙점으로 설정
    points.forEach(point => {
        if (point !== top && point !== bottom && point !== left && point !== right) {
            centerPoint = point;
        }
    });

    return [top, left, centerPoint, right, bottom];
}
window.order;

// 클릭된 버튼 집합에서 도형을 감지하는 함수
function detectShapeFromClickedButtons(clickedButtons) {
    const points = Array.from(clickedButtons).map(el => getElementCenter(el));
    const tolerance = 170;

    console.log('Points:', points);

    if (points.length === 3) {
        const cardOrder = Array.from(clickedButtons)
            .map(el => ({ element: el, center: getElementCenter(el) }))
            .sort((a, b) => a.center.x - b.center.x)
            .map(item => parseInt(item.element.id.match(/button-(\d+)/)[1]));
            window.order=cardOrder;
        if (isTriangle(points, tolerance)) {
            if (cardOrder[0] === 8 && cardOrder[1] === 7 && cardOrder[2] === 6) {
                console.log('The clicked buttons form an Oracle spread.');
                
                return 'Oracle';
            } else if (cardOrder[0] === 7 && cardOrder[1] === 8 && cardOrder[2] === 6) {
                console.log('The clicked buttons form a Fortune spread.');
                return 'Fortune';
            } else {
                console.log('The clicked buttons form a triangle.');
                return 'Triangle';
            }
        } else {
            console.log('The clicked buttons do not form a triangle.');
            return 'Error';
        }
    } else if (points.length === 5) {
        const [top, left, centerPoint, right, bottom] = determineOrder(points);

        // 각 버튼의 ID를 판별된 순서에 맞게 정렬
        const cardOrder = [top, left, centerPoint, right, bottom].map(p => {
            const element = Array.from(clickedButtons).find(el => {
                const center = getElementCenter(el);
                return center.x === p.x && center.y === p.y;
            });
            return parseInt(element.id.match(/button-(\d+)/)[1]);
        });

        console.log('Card Order:', cardOrder);
        window.order=cardOrder;
        if (isCross(points, tolerance)) {
            if (cardOrder.toString() === [8, 7, 4, 5, 6].toString()) {
                console.log('The clicked buttons form a Star spread.');
                return 'Star';
            } else if (cardOrder.toString() === [4,7,8,6,5].toString()) {
                console.log('The clicked buttons form a Future 2 spread.');
                return 'Future-2';
            } else {
                console.log('The clicked buttons form a cross.');
                return 'Cross';
            }
        } else {
            console.log('The clicked buttons do not form a cross.');
            return 'Error';
        }
    } else if (points.length === 4) {
        const cardOrder = Array.from(clickedButtons)
            .map(el => ({ element: el, center: getElementCenter(el) }))
            .sort((a, b) => a.center.x - b.center.x)
            .map(item => parseInt(item.element.id.match(/button-(\d+)/)[1]));
        window.order=cardOrder;
        if (cardOrder[0] === 8 && cardOrder[1] === 7 && cardOrder[2] === 6 && cardOrder[3] === 5) {
            console.log('The clicked buttons form a Future spread.');
            return 'Future-1';
        } else {
            console.log('The clicked buttons do not form a recognized spread.');
            return 'Triangle';
        }
    } else {
        console.log('Unsupported number of clicked buttons.');
        return 'error';
    }
}

// 문서가 로드된 후 도형 감지 수행
document.addEventListener('DOMContentLoaded', () => {
    const positionCheckButton = document.querySelector('#positioncheck');
    if (positionCheckButton) {
        positionCheckButton.addEventListener('click', () => {
            detectShapeFromClickedButtons(clickedButtons);
        });
    } else {
        console.log('Position check button not found.');
    }
});