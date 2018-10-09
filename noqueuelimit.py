import queue
import numpy.random
import time
import random
# process_start 


class simulation:

	def __init__(self):
		self.id_sequence=0
		self.queue_list=[]
		self.fulltime = 0
		self.startexpotime = 3 
		self.processtimetime = 5
		self.processtime_queue = queue.Queue()
		self.queue_maxlength = 20
		self.leftstarttime = 0


	def process_start(self):

		self.id_sequence+=1
		starttime = numpy.random.exponential(self.startexpotime)
		#starttime = 1
		processtime = numpy.random.exponential(self.processtimetime)
		#processtime = 2
		testdiction = {'id':self.id_sequence, 'starttime': starttime, 'recenttime' : self.leftstarttime+starttime , 'waitingtime':0, 'processtime':processtime}

		self.leftstarttime += starttime
		self.fulltime += starttime

		print("만들어졌을때 : ",end='')
		return testdiction,starttime

	def process_first(self,diction,starttime):

		if((self.fulltime-starttime-diction['recenttime'])>0):
			print("delayed..")
			diction['waitingtime'] = self.fulltime-starttime-diction['recenttime']

		self.processtime_queue.put(diction)
		
		processed_time = diction['processtime']
		self.fulltime += processed_time
		if not self.processtime_queue.empty():
			diction = self.processtime_queue.get()
		return diction

	def process_end(self,diction):


		print("기다린시간 : " +str(diction['waitingtime']) ,end= ' ,')
		print("생성된 시간 : " +str(diction['recenttime']) ,end= ' ,')
		print("프로세스가 끝났을 때 시간: " +str(diction['waitingtime']+diction['recenttime']+diction['processtime']),end= ' ,')
		print("종료 시간 :"+str(self.fulltime))
		diction['totaltime'] = self.fulltime-diction['recenttime']
		return diction

	def one_rotation(self):

		
		testdiction,starttime = self.process_start() #make
		self.queue_list.append(testdiction)
		print(len(self.queue_list))
		testdiction = self.process_first(self.queue_list[self.id_sequence-1],starttime)
		donediction = self.process_end(testdiction)
		print(donediction)
		self.queue_list[self.id_sequence-1]  = donediction


	def report(self):

		average_time = { 'starttime' : 0 , 'processtime' : 0, 'waitingtime':0, 'totaltime': 0}

		for num, diction in enumerate(self.queue_list):
			
			average_time['starttime']+=(diction['starttime'])
			average_time['processtime']+=(diction['processtime'])
			average_time['waitingtime']+=(diction['waitingtime'])
			average_time['totaltime']+=(diction['totaltime'])

		print("================total time===============")
		for key, value in average_time.items():

			print(key+' : '+str(value))

	def multi(self,num):
		for i in range(0,num):
			self.one_rotation()


	def reset(self):

		self.queue_list.clear()

if __name__ == '__main__':
	
	noqueuelimit = simulation()
	noqueuelimit.multi(3)
	noqueuelimit.report()
	noqueuelimit.reset()
	noqueuelimit.report()

