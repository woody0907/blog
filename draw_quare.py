import turtle

def draw_squar(brad):
	for i in range(1,5):
		brad.forward(100)
		brad.right(90)


def draw_art():
	window = turtle.Screen()
	window.bgcolor("red")
	brad = turtle.Turtle()
	brad.color("yellow")
	brad.shape("turtle")
	for i in range(1,37):
		draw_squar(brad)	
		brad.right(10)
	window.exitonclick()

draw_art()