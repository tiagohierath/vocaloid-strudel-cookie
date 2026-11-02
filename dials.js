// Pointer capture keeps mouse, pen and touch drags attached to one control.
// https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events
window.bindDial = function (element, read, write, min = 0, max = 100, pixels = 8) {
  let drag = null;
  const set = value => write(Math.max(min, Math.min(max, Math.round(value))));
  element.onpointerdown = event => {
    if (event.button !== 0 || drag) return;
    event.preventDefault();
    element.focus({preventScroll:true});
    drag = {id:event.pointerId, y:event.clientY, value:read(), moved:false};
    element.setPointerCapture(event.pointerId);
  };
  element.onpointermove = event => {
    if (!drag || drag.id !== event.pointerId) return;
    const distance = drag.y - event.clientY;
    if (Math.abs(distance) > 3) drag.moved = true;
    if (drag.moved) set(drag.value + distance / pixels);
  };
  element.onpointerup = event => {
    if (!drag || drag.id !== event.pointerId) return;
    if (!drag.moved) set(read() + 1);
    drag = null;
    if (element.hasPointerCapture(event.pointerId)) element.releasePointerCapture(event.pointerId);
  };
  element.onpointercancel = element.onlostpointercapture = () => { drag = null; };
  element.onkeydown = event => {
    const changes = {ArrowUp:1, ArrowRight:1, ArrowDown:-1, ArrowLeft:-1};
    if (event.key in changes) { event.preventDefault(); set(read() + changes[event.key]); }
    else if (event.key === 'Home' || event.key === 'End') {
      event.preventDefault(); set(event.key === 'Home' ? min : max);
    }
  };
};
