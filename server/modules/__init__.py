def named_tuple_to_dict(tple):
	data = {}
	for f in tple._asdict().items():
		if isinstance(f, tuple):
			k, v = f
			data[k] = v
		else:
			for k1, v1 in f:
				data[k1] = v1
	return data
