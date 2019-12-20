$('.parent-control').click(function () {
    $(this).toggleClass('fa-caret-right');
    $(this).parent().parent().nextUntil('.parent').attr({hidden:function(index, attr){
    return attr === 'hidden' ? null : 'hidden';
}});
});