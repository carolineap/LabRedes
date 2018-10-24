#Laboratório de Redes de Computadores - Implementação RIP
#Caroline Aparecida de Paula Silva - 726506
#Isabela Sayuri Matsumoto - 726539

MCAST_GRP = '127.0.0.1'
MCAST_PORT = 2048

import sys
import socket
import threading
import numpy
import pickle
import time

class Packet():
		
	def __init__(self, sourceid, destid, mincost):
		
		self.sourceid = sourceid
		self.destid = destid
		self.mincost = mincost


class Node():

	def __init__(self, nid, myCosts):
		
		threading.Thread.__init__(self)
		

		ttl = 1
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, ttl)
		sock.bind((MCAST_GRP, MCAST_PORT + nid))

		self.id = nid
		self.socket = sock
		self.myCosts = myCosts
		self.adj = []
		self.costs = numpy.empty(shape=(4,4))
		self.costs.fill(999)


		for i in range(4):
			if self.myCosts[i] != 999 and i != self.id:
				self.adj.append(i)
			self.costs[i][i] = 0
			self.costs[nid][i] = myCosts[i]
			self.costs[i][nid] = myCosts[i]


	def updateTable(self, i, j, cost):
		self.costs[i][j] = cost
		self.costs[j][i] = cost

	def printCost(self):
		print("I am node " + str(self.id) + " and my costs are " + str(self.myCosts))

	def printTable(self):		
		print("I am node " + str(self.id) + " and my table is \n" + str(self.costs))

class Sender(threading.Thread):

	def __init__(self, node):

		threading.Thread.__init__(self)
		self.socket = node.socket
		self.node = node


	def run(self):
		
		#while True:
			for a in self.node.adj:
				try:
					packet = Packet(self.node.id, a, self.node.myCosts)
					self.socket.sendto(pickle.dumps(packet),(MCAST_GRP, MCAST_PORT + a))
				except:
					print("I am trying to send a message...")
				else:
					time.sleep(2)


class Receiver(threading.Thread):

	def __init__(self, node):

		threading.Thread.__init__(self)
		self.node = node
		self.socket = node.socket

	def run(self):
		
		while(True):
			try: 
				data, addr = self.socket.recvfrom(1024)
				packet = pickle.loads(data)
			except:
				print("Waiting for new packet...")
			else:
				
				for i in range(4):

					self.node.updateTable(packet.sourceid, i, packet.mincost[i])

					if (self.node.myCosts[i] > packet.mincost[i] + self.node.myCosts[packet.sourceid]):
						self.node.myCosts[i] = packet.mincost[i] + self.node.myCosts[packet.sourceid]
						self.node.updateTable(self.node.id, i, self.node.myCosts[i])
						self.node.printCost()

				self.node.printTable()
				


def main():

	node0 = Node(0, [0, 1, 3, 7])
	node1 = Node(1, [1, 0, 1, 999])
	node2 = Node(2, [3, 1, 0, 2])
	node3 = Node(3, [7, 999, 2, 0])

	node0.printTable()
	node1.printTable()
	node2.printTable()
	node3.printTable()


	sender0 = Sender(node0)
	receiver0 = Receiver(node0)
	sender0.start()
	receiver0.start()

	sender1 = Sender(node1)
	receiver1 = Receiver(node1)
	sender1.start()
	receiver1.start()

	sender2 = Sender(node2)
	receiver2 = Receiver(node2)
	sender2.start()
	receiver2.start()

	sender3 = Sender(node3)
	receiver3 = Receiver(node3)
	sender3.start()
	receiver3.start()


if __name__ == "__main__": main()




