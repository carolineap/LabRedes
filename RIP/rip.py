#Laboratório de Redes de Computadores - Implementação RIP
#Caroline Aparecida de Paula Silva - 726506
#Isabela Sayuri Matsumoto - 726539

MCAST_GRP = '127.0.0.1'
MCAST_PORT = 2048


import sys
import socket
import numpy
import pickle
import time

class Packet():
		
	def __init__(self, sourceid, destid, mincost):
		
		self.sourceid = sourceid
		self.destid = destid
		self.mincost = mincost


class Node():


	def __init__(self, nid, myCosts, socket):

		self.id = nid
		self.myCosts = myCosts
		self.adj = []
		self.costs = numpy.empty(shape=(4,4))
		self.costs.fill(999)
		self.socket = socket

		for i in range(4):
			if self.myCosts[i] != 999 and i != self.id:
				self.adj.append(i)	
			self.updateTable(i, i, 0)
			self.updateTable(nid, i, myCosts[i])

		print("My adj are " + str(self.adj))
		update = 1

		send(socket, self)

	def updateTable(self, i, j, cost):
		self.costs[i][j] = cost
		self.costs[j][i] = cost

	def printCost(self):
		print("I am node " + str(self.id) + " and my costs are " + str(self.myCosts))

	def printTable(self):		
		print("I am node " + str(self.id) + " and my table is \n" + str(self.costs))


def send(socket, node):
	
	for a in node.adj:
		packet = Packet(node.id, a, node.myCosts)
		print("Send packet to node " + str(a) + " with myCosts = " + str(node.myCosts))
		socket.sendto(pickle.dumps(packet),(MCAST_GRP, MCAST_PORT + a))

def receiver(socket, node):
	
	while(True):
		try: 
			data, addr = socket.recvfrom(1024)
			packet = pickle.loads(data)
			print("Received packet from " + str(packet.sourceid) + " with cost = " + str(packet.mincost))
		except:
			print("Waiting for new packet...")
		else:	
			for i in range(4):
				node.updateTable(packet.sourceid, i, packet.mincost[i])
				if (node.myCosts[i] > packet.mincost[i] + node.myCosts[packet.sourceid]):
					print("Update my table from " + str(node.myCosts[i]) + "to " + str(packet.mincost[i] + node.myCosts[packet.sourceid]))
					node.myCosts[i] = packet.mincost[i] + node.myCosts[packet.sourceid]
					node.updateTable(node.id, i, node.myCosts[i])
					node.printCost()
					send(socket, node)
			node.printTable()
				


def main():

	nid = int(sys.argv[1])

	ttl = 1
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, ttl)
	sock.bind((MCAST_GRP, MCAST_PORT + nid))


	if (nid == 0):
		node = Node(nid, [0, 1, 3, 7], sock)
	elif (nid == 1):
		node = Node(nid, [1, 0, 1, 999], sock)
	elif (nid == 2):
		node = Node(nid, [3, 1, 0, 2], sock)
	elif (nid == 3):
		node = Node(nid, [7, 999, 2, 0], sock)

	time.sleep(7)
	node.printTable()

	receiver(sock, node)
	receiver.start()
	

if __name__ == "__main__": main()




