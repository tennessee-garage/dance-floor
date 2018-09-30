function handleError(error) {
    console.error(error);
}

// Quirk: Un-focus bootstrap buttons after click.
$(".btn").mouseup(function(){
  $(this).blur();
});
