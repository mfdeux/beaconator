/**
 * Move scroll bar from screen
 */
export function bodyFreezeScroll() {
  const body = document.body
  body.style.marginRight = '15px'
  body.style.overflow = 'hidden'
}

/**
 * Move scroll bar back
 */
export function bodyUnfreezeScroll() {
  const body = document.body
  body.style.marginRight = '0px'
  body.style.overflow = 'auto'
}
