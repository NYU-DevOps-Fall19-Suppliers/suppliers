
let pointer = root 
while not found x: 
	if x is in keyset(pointer):
		let pointer = root
	else: 
		if x in inset(pointer):	
			if x in edgeset(pointer, node):
				let pointer = node 
		else: 
			let pointer = parent 
return x

entering elevator:

SELECT COUNT(*) INTO :num FROM Status 
WHERE InElevator='N'
IF num > 9 ROLLBACK 
INSERT Status 
	InElevator = ’Y’ 
	WHERE UID =:U
COMMIT