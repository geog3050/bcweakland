def plantStatus(climate, temps):
	if climate == "Tropical":
		threshold = 30
	elif climate == "Continental":
		threshold = 25
	else:
		threshold = 18
		
	for x in temps:
		if x <= threshold:
			print("F")
		else:
			print("U")
			