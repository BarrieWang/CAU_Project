/*
 * @Author: Vincent
 * @Date: 2020-03-04 16:49:58
 * @LastEditTime: 2020-03-04 17:02:37
 * @LastEditors: Please set LastEditors
 * @Description: javascripts utils
 * @FilePath: \CAU_Project\static\util.js
 */
function hasClass(element, clssname) {
    return element.className.match(new RegExp('(\\s|^)' + clssname + '(\\s|$)'));
}
function addClass(element, clssname) {
    if (!this.hasClass(element, clssname)) element.className += ' ' + clssname;
}
function removeClass(element, clssname) {
    if (hasClass(element, clssname)) {
        var reg = new RegExp('(\\s|^)' + clssname + '(\\s|$)');
        element.className = element.className.replace(reg, ' ');
    }
}
function toggleClass(element, clssname) {
    if (hasClass(element, clssname)) {
        removeClass(element, clssname);
    } else {
        addClass(element, clssname);
    }
}