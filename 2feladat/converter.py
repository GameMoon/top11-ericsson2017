from PIL import Image

class OutputGenerator:

    def convert(self, cells, units, enemies):
        output = [-2]*80*100 # vector with 80*100 size

        for x in range(len(cells)):
            for y in range(len(cells[x])):
                # Position in the output vector
                current_index = y+x*100

                # Attackable field
                if cells[x][y].owner != 1 and cells[x][y].attack.which() == "can" and cells[x][y].attack.can is True:
                    output[current_index] = 0
                # Unit capturing line
                if cells[x][y].attack.which() == "unit" and units[cells[x][y].attack.unit].owner == 1:
                    output[current_index] = cells[x][y].attack.unit+(len(units)-1)*3+2
                # Our fields
                if cells[x][y].owner == 1 and cells[x][y].attack.which() == "can" and cells[x][y].attack.can is True:
                    output[current_index] = -1

        for unit_index in range(len(units)):
            unit = units[unit_index]
            if unit.owner == 1:
                output[unit.position.x*100 + unit.position.y] = unit_index+(len(units)-1)*3+2 + unit.health
            else:
                output[unit.position.x * 100 + unit.position.y] = 1

        for enemy in enemies:
            output[enemy.position.x * 100 + enemy.position.y] = 1

        return output

    def show(self, output):
        row = [None]*100
        tempindex = 0

        for index in range(len(output)):

            row[tempindex] = output[index]

            if tempindex == 99:
                print(row)
                tempindex = 0
            else:
                tempindex = tempindex + 1

    def create_image(self, output,tick):
        image_array = [None]*len(output)

        for index in range(len(output)):
            if output[index] == -1:
                image_array[index] = (0, 0, 0)
            elif output[index] == 0:
                image_array[index] = (255, 255, 255)
            elif output[index] == -2:
                image_array[index] = (0, 0, 255)
            elif output[index] == 1:
                image_array[index] = (255, 0, 0)
            elif output[index] == 2 or output[index] == 6:
                image_array[index] = (255, 255, 0)
            else:
                image_array[index] = (0, 255, 0)

        img = Image.new('RGB', (100, 80))
        img.putdata(image_array)
        img.save('images/output_'+str(tick)+'.png')