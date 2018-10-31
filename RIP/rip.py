#Laboratório de Redes de Computadores - Implementação RIP
#Caroline Aparecida de Paula Silva - 726506
#Isabela Sayuri Matsumoto - 726539

MCAST_GRP = '127.0.0.1'
MCAST_PORT = 2048

import threading
import sys
import socket
import numpy
import pickle
import time
import random

class Packet(): ## Estrutura do pacote a ser enviado e recebido rtpkt
		
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

		for i in range(4):	#inicializando tabela
			if self.myCosts[i][0] != 999 and i != self.id:
				self.adj.append(i)	

		print("My adjacencies are " + str(self.adj))
		update = 1

	def updateTable(self, i, cost, nextHop): # rtupdate
		self.myCosts[i][0] = cost 
		self.myCosts[i][1] = nextHop

	def printCost(self):
		print("I am node " + str(self.id) + " and my costs are " + str(self.myCosts))

	def printTable(self):		
		print("\n")
		#print("I am node " + str(self.id) + " and my table is" )
		for i in range(4):
			print(self.myCosts[i])
		print("\n")


def send(socket, node):
	
	for a in node.adj:
		packet = Packet(node.id, a, node.myCosts)
		print("Send packet to node " + str(a) + " with myCosts = " + str(node.myCosts))
		socket.sendto(pickle.dumps(packet),(MCAST_GRP, MCAST_PORT + a))

class Receiver(threading.Thread):
	def __init__(self, sock, node):
		threading.Thread.__init__(self)
		self.node = node
		self.socket = sock

	def run(self):

		while(True):
			try: 
				data, addr = self.socket.recvfrom(1024)
				packet = pickle.loads(data)
				print("Received packet from " + str(packet.sourceid) + " with cost = " + str(packet.mincost))
			except:
				print("Waiting for new packet...")
				
			else:	
				flag = False
				for i in range(4):
					#node.updateTable(i, packet.mincost[i][0], packet)
					if (self.node.myCosts[i][0] > packet.mincost[i][0] + self.node.myCosts[packet.sourceid][0]): # se o custo que eu recebi é menor
						print("Update my table node " + str(i) + " cost from " + str(self.node.myCosts[i][0]) + " to cost " + str(packet.mincost[i][0] + self.node.myCosts[packet.sourceid][0]))
						print("Update my table node " + str(i) + " hop from " + str(self.node.myCosts[i][1]) + " to next hop " + str(self.node.myCosts[packet.sourceid][1]))
						self.node.updateTable( i, packet.mincost[i][0]+self.node.myCosts[packet.sourceid][0], self.node.myCosts[packet.sourceid][1])#.mincost[i][1]) #Atualiza na tabela
						flag = True
				if(flag==True):		
					send(self.socket, self.node)
				self.node.printTable()
				


def main():
	
	nid = int(sys.argv[1])
	ttl = 1
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, ttl)
	sock.bind((MCAST_GRP, MCAST_PORT + nid))

	if (nid == 0):
		node = Node(nid, [[0,0], [1,1], [3,2], [7,3]], sock)
	elif (nid == 1):
		node = Node(nid, [[1,0], [0,1], [1,2], [999, None]], sock)
	elif (nid == 2):
		node = Node(nid, [[3,0], [1,1], [0,2], [2,3]], sock)
	elif (nid == 3):
		node = Node(nid, [[7,0], [999, None], [2,2], [0,3]], sock)

	
	node.printTable()
	
	receiver = Receiver(sock, node)
	receiver.start()
	time.sleep(7)
	send(sock, node)



if __name__ == "__main__": main()




