import struct
class Constant(object):
	constant_pool = [None,]
	def __init__(self,tag):
		self.tag = tag
		self.constant_pool.append(self)
	def __str__(self):
		if hasattr(self,'value'):
			return '%d====>%s'% (self.tag,self.value,)
		else:
			return super(Constant,self).__str__()
class ConstantClassref(Constant):
	@staticmethod
	def _nextStep():
		return (2,)
	def __init__(self,tag,data_tuple):
		Constant.__init__(self,tag)
		self.utf8_index = struct.unpack('>H',''.join(data_tuple))[0]
	def indexToValue(self):
		if hasattr(self,'value'):
			return
		cutf8 = self.constant_pool[self.utf8_index]
		assert isinstance(cutf8, ConstantUtf8)
		self.value = self.classinfo = cutf8.value

class ConstantInteger(Constant):
	@staticmethod
	def _nextStep():
		return (4,)
	def __init__(self, tag, data_tuple):
		Constant.__init__(self,tag)
		self.int_value = struct.unpack('>I',''.join(data_tuple))[0]
	def indexToValue(self):
		self.value = self.int_value

class ConstantLong(Constant):
	@staticmethod
	def _nextStep():
		return (4,4,)
	def __init__(self,tag, data_tuple):
		Constant.__init__(self,tag)
		self.long_value = struct.unpack('>L',''.join(data_tuple))[0]
	def indexToValue(self):
		self.value = self.long_value
	
class ConstantFloat(Constant):
	@staticmethod
	def _nextStep():
		return (4,)
	def __init__(self, tag, data_tuple):
		Constant.__init__(self,tag)
		self.float_value = struct.unpack('>f',''.join(data_tuple))[0]
	def indexToValue(self):
		self.value = self.float_value

class ConstantDouble(Constant):
	@staticmethod
	def _nextStep():
		return (4,4,)
	def __init__(self, tag, data_tuple):
		Constant.__init__(self, tag)
		self.double_value = struct.unpack('>d',''.join(data_tuple))[0]
	def indexToValue(self):
		self.value = self.double_value
class ConstantString(Constant):
	@staticmethod
	def _nextStep():
		return (2,)
	def __init__(self, tag, data_tuple):
		Constant.__init__(self,tag)
		self.utf8_index = struct.unpack('>H',''.join(data_tuple))[0]
	def indexToValue(self):
		cutf8=self.constant_pool[self.utf8_index]
		assert isinstance(cutf8, ConstantUtf8)
		self.value=cutf8.value
	
class ConstantFieldref(Constant):
	@staticmethod
	def _nextStep():
		return (2,2,)
	def __init__(self, tag, data_tuple):
		Constant.__init__(self,tag)
		self.class_index = struct.unpack('>H',data_tuple[0])[0]
		self.name_and_type_index = struct.unpack('>H',data_tuple[1])[0]
	def indexToValue(self):
		classClass = self.constant_pool[self.class_index]
		assert isinstance(classClass, ConstantClassref)
		if not hasattr(classClass, 'value'):
			classClass.indexToValue()
		self.classinfo=classClass.value
		cnameandtype = self.constant_pool[self.name_and_type_index]
		assert isinstance(cnameandtype, ConstantNameAndType)
		if not hasattr(cnameandtype, 'value'):
			cnameandtype.indexToValue()
		self.name_and_type = cnameandtype.value
		self.value=(self.classinfo, self.name_and_type)

class ConstantMethodref(Constant):
	@staticmethod
	def _nextStep():
		return (2,2,)
	def __init__(self, tag, data_tuple):
		Constant.__init__(self, tag)
		self.class_index = struct.unpack('>H',data_tuple[0])[0]
		self.name_and_type_index = struct.unpack('>H',data_tuple[1])[0]
	def indexToValue(self):	
		classClass = self.constant_pool[self.class_index]
		assert isinstance(classClass, ConstantClassref)
		if not hasattr(classClass, 'value'):
			classClass.indexToValue()
		self.classinfo=classClass.value
		cnameandtype = self.constant_pool[self.name_and_type_index]
		assert isinstance(cnameandtype, ConstantNameAndType)
		if not hasattr(cnameandtype, 'value'):
			cnameandtype.indexToValue()
		self.name_and_type = cnameandtype.value
		self.value=(self.classinfo, self.name_and_type)


class ConstantInterfaceMethodref(Constant):
	@staticmethod
	def _nextStep():
		return (2,2,)
	def __init__(self, tag, data_tuple):
		Constant.__init__(self, tag)
		self.class_index = struct.unpack('>H', data_tuple[0])[0]
		self.name_and_type_index = struct.unpack('>H',data_tuple[1])[0]
	
	def indexToValue(self):
		classClass = self.constant_pool[self.class_index]
		assert isinstance(classClass, ConstantClassref)
		if not hasattr(classClass, 'value'):
			classClass.indexToValue()
		self.classinfo=classClass.value
		cnameandtype = self.constant_pool[self.name_and_type_index]
		assert isinstance(cnameandtype, ConstantNameAndType)
		if not hasattr(cnameandtype, 'value'):
			cnameandtype.indexToValue()
		self.name_and_type = cnameandtype.value
		self.value=(self.classinfo, self.name_and_type)

class ConstantNameAndType(Constant):
	@staticmethod
	def _nextStep():
		return (2,2,)
	def __init__(self, tag, data_tuple):
		Constant.__init__(self, tag)
		self.name_index = struct.unpack('>H',data_tuple[0])[0]
		self.descriptor_index = struct.unpack('>H',data_tuple[1])[0]
	def indexToValue(self):
		if hasattr(self,'value'):
			return
		nameUTF8 = self.constant_pool[self.name_index]
		assert isinstance(nameUTF8, ConstantUtf8)
		self.name = nameUTF8.value
		descriptorUTF8 = self.constant_pool[self.descriptor_index]
		assert isinstance(descriptorUTF8, ConstantUtf8)
		self.descriptor = descriptorUTF8.value
		self.value = (self.name, self.descriptor,)

class ConstantUtf8(Constant):
	@staticmethod
	def _nextStep():
		return (2,0)
	def __init__(self, tag, data_tuple):
		Constant.__init__(self, tag)
		self.length = struct.unpack('>H', data_tuple[0])[0]
	
	def parseStringValue(self,raw_data):
		self.value = raw_data
		return self
	
	def indexToValue(self):
		pass

class Constants(Constant):
	"""
	Jvm class code CONSTANT
	"""
	CONSTANT_TYPE_MAP = {
		7:	ConstantClassref		,
		3:	ConstantInteger			,
		5:	ConstantLong			,
		4:	ConstantFloat			,
		6:	ConstantDouble			,
		8:	ConstantString			,
		9:	ConstantFieldref		,
		10:	ConstantMethodref		,
		11:	ConstantInterfaceMethodref	,
		12:	ConstantNameAndType		,
		1:	ConstantUtf8			,
	}
	@classmethod
	def nextStep(cls,tag):
		assert tag in cls.CONSTANT_TYPE_MAP
		return cls.CONSTANT_TYPE_MAP[tag]._nextStep()

	@classmethod
	def createConstant(cls,tag,data_tuple):
		assert tag in cls.CONSTANT_TYPE_MAP
		return cls.CONSTANT_TYPE_MAP[tag](tag,data_tuple)
	@classmethod
	def indexToValue(cls):
		for cons in cls.constant_pool:
			if hasattr(cons,'indexToValue'):
				cons.indexToValue()
