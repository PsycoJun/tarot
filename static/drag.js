document.addEventListener('DOMContentLoaded', (event) => {
    const draggables = document.querySelectorAll('.draggable');
    const container = document.querySelector('#card-container');
    const card = document.querySelector('.card');

    function isElementInContainer(container, element) {
        const containerRect = container.getBoundingClientRect();
        const elementRect = element.getBoundingClientRect();
    
        return (
            elementRect.top >= containerRect.top &&
            elementRect.left >= containerRect.left &&
            elementRect.bottom <= containerRect.bottom &&
            elementRect.right <= containerRect.right
        );
    }
    
    draggables.forEach(draggable => {
        draggable.addEventListener('mousedown', (e) => {
            draggable.style.cursor = 'grabbing';

            let initialX = e.clientX;
            let initialY = e.clientY;
            let startX = draggable.offsetLeft;
            let startY = draggable.offsetTop;
            let shiftX = initialX - startX;
            let shiftY = initialY - startY;

            function moveAt(pageX, pageY) {
                draggable.style.left = pageX - shiftX + 'px';
                draggable.style.top = pageY - shiftY + 'px';
            }

            function onMouseMove(e) {
                moveAt(e.pageX, e.pageY);
                

                if (container && card) {
                    if (isElementInContainer(container, draggable)) {
                        if (!clickedButtons.has(draggable)) {
                            clickedButtons.add(draggable);
                            console.log('Added to insideElements:', clickedButtons);
                        }
                    } else {
                        if (clickedButtons.has(draggable)) {
                            clickedButtons.delete(draggable);
                            console.log('Removed from insideElements:', draggable);
                        }
                    }
                } else {
                    console.log('Container or card element not found.');
                }
            }

            document.addEventListener('mousemove', onMouseMove);

            document.addEventListener('mouseup', () => {
                document.removeEventListener('mousemove', onMouseMove);
                draggable.style.cursor = 'grab';
            }, { once: true });
        });

        draggable.addEventListener('dragstart', () => {
            return false;
        });
    });
});
