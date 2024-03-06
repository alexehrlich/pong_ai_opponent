import pygame
from pong import Game
import neat
import os
import pickle
import time


class PongGame:
	def __init__(self, window, width, height):
		self.game = Game(window, width, height)
		self.left_paddle = self.game.left_paddle
		self.right_paddle = self.game.right_paddle
		self.ball = self.game.ball
	
	def predict_y_on_ai_paddleside(self):
		kathete = (self.ball.y_vel/self.ball.x_vel) * (self.game.window_width - (self.game.window_width - self.right_paddle.x) - self.ball.x)
		if (self.ball.y_vel == 0):
			return self.ball.y
		y_virtual_hit = self.ball.y + kathete #can be negative depending on speed_y --> is dann subtracted correctly
		if (y_virtual_hit < 0):
			y_virtual_hit *= -1
		if ((y_virtual_hit // self.game.window_height) % 2 == 0):
			return y_virtual_hit % self.game.window_height
		elif ((y_virtual_hit // self.game.window_height) % 2 != 0):
			return self.game.window_height - (y_virtual_hit % self.game.window_height)

	def test_ai(self, genome, config):
		net = neat.nn.FeedForwardNetwork.create(genome, config)

		run = True
		clock = pygame.time.Clock()
		start_time = time.time()
		decision = 0
		predicted_y_ai = 0
		while run:
			clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					break

			keys = pygame.key.get_pressed()
			if keys[pygame.K_w]:
				self.game.move_paddle(left=True, up=True)
			if keys[pygame.K_s]:
				self.game.move_paddle(left=True, up=False)

			if (time.time() - start_time >= 1):
				if (self.ball.x_vel < 0):
					output = net.activate(
						(self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
					decision = output.index(max(output))
				else:
					predicted_y_ai = self.predict_y_on_ai_paddleside()
				start_time = time.time()

			if (self.ball.x_vel < 0):
				if decision == 0:
					pass
				elif decision == 1:
					self.game.move_paddle(left=False, up=True)
				else:
					self.game.move_paddle(left=False, up=False)
			else:
				if ((self.right_paddle.y + self.right_paddle.HEIGHT / 2 > predicted_y_ai) and (self.right_paddle.y > 0)):
					self.game.move_paddle(left=False, up=True)
				elif((self.right_paddle.y + self.right_paddle.HEIGHT / 2 < predicted_y_ai) and (self.right_paddle.y < self.game.window_height - self.right_paddle.HEIGHT)):
					self.game.move_paddle(left=False, up=False)
				else:
					pass

			game_info = self.game.loop()
			self.game.draw(True, False)
			pygame.display.update()

		pygame.quit()

	def train_ai(self, genome1, genome2, config):
		net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
		net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

		run = True
		while run:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit()

			output1 = net1.activate(
				(self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
			decision1 = output1.index(max(output1))

			if decision1 == 0:
				pass
			elif decision1 == 1:
				self.game.move_paddle(left=True, up=True)
			else:
				self.game.move_paddle(left=True, up=False)

			output2 = net2.activate(
				(self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
			decision2 = output2.index(max(output2))

			if decision2 == 0:
				pass
			elif decision2 == 1:
				self.game.move_paddle(left=False, up=True)
			else:
				self.game.move_paddle(left=False, up=False)

			game_info = self.game.loop()

			self.game.draw(draw_score=False, draw_hits=True)
			pygame.display.update()

			if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.left_hits > 50:
				self.calculate_fitness(genome1, genome2, game_info)
				break

	def calculate_fitness(self, genome1, genome2, game_info):
		genome1.fitness += game_info.left_hits
		genome2.fitness += game_info.right_hits


def eval_genomes(genomes, config):
	width, height = 700, 500
	window = pygame.display.set_mode((width, height))

	for i, (genome_id1, genome1) in enumerate(genomes):
		if i == len(genomes) - 1:
			break
		genome1.fitness = 0
		for genome_id2, genome2 in genomes[i+1:]:
			genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
			game = PongGame(window, width, height)
			game.train_ai(genome1, genome2, config)


def run_neat(config):
	p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-7')
	#p = neat.Population(config)
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	p.add_reporter(neat.Checkpointer(1))

	winner = p.run(eval_genomes, 1)
	with open("best.pickle", "wb") as f:
		pickle.dump(winner, f)


def test_ai(config):
	width, height = 700, 500
	window = pygame.display.set_mode((width, height))

	with open("best.pickle", "rb") as f:
		winner = pickle.load(f)

	game = PongGame(window, width, height)
	game.test_ai(winner, config)


if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config.txt")

	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_path)
	# run_neat(config)
	test_ai(config)
