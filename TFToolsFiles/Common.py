from Error import Error, ERRCODE

def RepeatKeys(filename, object):
	errList = []
	knownKeys = []

	for key in object:
		if key in knownKeys:
			print(f"duplicate key {key}")
			errList.append(Error(ERRCODE.OBJECT_KEYS_DUPLICATED, filename,
								 f"Duplicate key {key} found in object"))
		else:
			knownKeys.append(key)

	return len(errList), errList
