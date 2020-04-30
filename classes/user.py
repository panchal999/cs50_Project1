class User:
	def __init__(self,id,name,emailid,password):
		self.id=id;
		self.name=name
		self.emailid=emailid
		self.password=password

	def __repr__(self):
		return f'<User:{self.emailid}>'


# users=[]

# users.append(User(id=1,emailid="abc@gmail.com",password="123"))
# users.append(User(id=2,emailid="def@gmail.com",password="123"))


# print(users)