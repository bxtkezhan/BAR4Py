var RotateTag = 0;
function animate(id, model) {
    if (id == '701') {
        model.rotateX(Math.PI/2);
        model.rotateY(RotateTag);
        RotateTag += 0.1;
	}
}
