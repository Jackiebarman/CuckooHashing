import math
class CuckooHash:
	
	def __init__(self,size=1000):
		self.len=size
		self.hashtable=[[None for _ in range(self.len)] for _ in range(3)]
		self.stash=CuckooHash(self.len//10) if self.len>=10 else None	
		self.population=0

	def stringHashFunction(self,key):
		key = key.lower()
		p1=37
		sum1,sum2,sum3=37,5381,0
		for i in range(len(key)-1,-1,-1):
			sum1 = (sum1+ord(key[i]))*p1   #return an integer representing the Unicode code point of the character when the argument is a unicode object
			sum2 = ((sum2 << 5) + sum2) + ord(key[i])
			sum3 = ord(key[i]) + (sum3 << 6) + (sum3 << 16) - sum3             #ord('a') returns the integer 97
		sum1=sum1%self.len
		sum2=sum2%self.len
		sum3=sum3%self.len
		return (sum1,sum2,sum3)

	def integerHashFunction(self,key): 
		return self.stringHashFunction(str(key))

	def insert(self,data,count=0,i=0):
		if self.stash is not None and (count>math.floor(math.log(self.len))):
			self.stash.insert(data)				
			return
			
		if(isinstance(data[0],int)):
			hashvalues=self.integerHashFunction(data[0])
			
		else:
			data[0] = data[0].lower()
			hashvalues=self.stringHashFunction(data[0])
			
		if(self.hashtable[i][hashvalues[i]]==None):
			self.hashtable[i][hashvalues[i]]=data
			
		else:
			temp=self.hashtable[i][hashvalues[i]]
			self.hashtable[i][hashvalues[i]]=data
			self.insert(temp,count+1,(i+1)%3)
			
		self.population += 1
		if self.population>self.len*0.9*3:
			self.rehash()

	def delete(self,key):
		if self.lookup(key):
			if isinstance(key,int):
				hashvalues = self.integerHashFunction(key)
				
			else:
				key = key.lower()
				hashvalues = self.stringHashFunction(key)
				
			if self.hashtable[0][hashvalues[0]] is not None and self.hashtable[0][hashvalues[0]][0]==key:
				self.hashtable[0][hashvalues[0]]=None
			elif self.hashtable[1][hashvalues[1]] is not None and self.hashtable[1][hashvalues[1]][0]==key:
				self.hashtable[1][hashvalues[1]]=None
			elif self.hashtable[2][hashvalues[2]] is not None and self.hashtable[2][hashvalues[2]][0]==key:
				self.hashtable[2][hashvalues[2]]=None
			elif self.stash is not None and self.stash.population>0:
				self.stash.delete(key)

	def lookup(self,key):
		if(isinstance(key,int)):
			hashvalues=self.integerHashFunction(key)
		else:
			key = key.lower()
			hashvalues=self.stringHashFunction(key)
		if self.hashtable[0][hashvalues[0]] is not None and self.hashtable[0][hashvalues[0]][0]==key:
			return True
		if self.hashtable[1][hashvalues[1]] is not None and self.hashtable[1][hashvalues[1]][0]==key:
			return True			
		if self.hashtable[2][hashvalues[2]] is not None and self.hashtable[2][hashvalues[2]][0]==key:
			return True			
		if self.stash is not None and self.stash.population>0:
			return self.stash.lookup(key)
		return False

	def getElements(self,elements=[]):
		for i in self.hashtable:
			for j in i:
				if j is not None:
					elements.append(j)
		if self.stash is not None and self.stash.population>0:
			elements = self.stash.getElements(elements)
		return elements

	def rehash(self):
		elements = self.getElements()
		LEN = 2*self.len
		self.hashtable[0] = [None] * LEN
		self.hashtable[1] = [None] * LEN
		self.hashtable[2] = [None] * LEN
		self.len=LEN
		self.population=0
		self.stash=CuckooHash(LEN//10) if LEN>=10 else None
		for i in elements:
			self.insert(i)

	def print(self):
		for i in range(3):
			print("Table ",i)
			for j in range(self.len):
				if self.hashtable[i][j] is not None:
					print(*self.hashtable[i][j])
		print("--------------------------------------------------------")
		if self.stash is not None and self.stash.population>0:
			print("Stash:")
			self.stash.print()


	def update(self,sign,key,val):
		if(isinstance(key,int)):
			hashvalues=self.integerHashFunction(key)
		else:
			key = key.lower()
			hashvalues=self.stringHashFunction(key)
		if sign=='+':
			if self.hashtable[0][hashvalues[0]][0]==key:
				self.hashtable[0][hashvalues[0]][1] += val
			elif self.hashtable[1][hashvalues[1]][0]==key:
				self.hashtable[1][hashvalues[1]][1] += val
			elif self.hashtable[2][hashvalues[2]][0]==key:
				self.hashtable[2][hashvalues[2]][1] += val
			elif self.stash.population>0:
				self.stash.update(sign,key,val)
		elif sign=='-':
			if self.hashtable[0][hashvalues[0]][0]==key:
				if self.hashtable[0][hashvalues[0]][1]>=val:
					self.hashtable[0][hashvalues[0]][1] -= val
				else:
					print("Invalid Data")
			elif self.hashtable[1][hashvalues[1]][0]==key:
				if self.hashtable[1][hashvalues[1]][1]>=val:
					self.hashtable[1][hashvalues[1]][1] -= val
				else:
					print("Invalid Data")
			elif self.hashtable[2][hashvalues[2]][0]==key:
				if self.hashtable[2][hashvalues[2]][1]>=val:
					self.hashtable[2][hashvalues[2]][1] -= val
				else:
					print("Invalid Data")
			elif self.stash.population>0:
				self.stash.update(sign,key,val)
