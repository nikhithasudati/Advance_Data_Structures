import sys

from ride import Ride_model
from min_heap import MinHeap
from min_heap import Min_Heap_NOde
from red_black_tree import Node,RBTree


def insert_ride(ride, heap, rbt):
    if rbt.get_ride(ride.rideNumber) is not None:
        output_add(None, "Duplicate RideNumber", False)
        sys.exit(0)
        return
    rbt_node = Node(None, None)
    min_heap_node = Min_Heap_NOde(ride, rbt_node, heap.curr_size + 1)
    heap.insert(min_heap_node)
    rbt.insert(ride, min_heap_node)

#adding output to the text file 
def output_add(ride, message, list):
    file = open("output_file.txt", "a")
    if ride is None:
        file.write(message + "\n")
    else:
        message = ""
        if not list:
            message += ("(" + str(ride.rideNumber) + "," + str(ride.rideCost) + "," + str(ride.tripDuration) + ")\n")
        else:
            if len(ride) == 0:
                message += "(0,0,0)\n"
            for i in range(len(ride)):
                if i != len(ride) - 1:
                    message = message + ("(" + str(ride[i].rideNumber) + "," + str(ride[i].rideCost) + "," + str(
                        ride[i].tripDuration) + "),")
                else:
                    message = message + ("(" + str(ride[i].rideNumber) + "," + str(ride[i].rideCost) + "," + str(
                        ride[i].tripDuration) + ")\n")

        file.write(message)
    file.close()

#print ride by given ridenumber
def print_ride(rideNumber, rbt):
    res = rbt.get_ride(rideNumber)
    if res is None:
        output_add(Ride_model(0, 0, 0), "", False)
    else:
        output_add(res.ride, "", False)

#print rides in range
def print_rides(l, h, rbt):
    list = rbt.get_rides_in_range(l, h)
    output_add(list, "", True)

#getnextride fromt the min_heap and deleting after getting it 
def get_next_ride(heap, rbt):
    if heap.curr_size != 0:
        popped_node = heap.pop()
        rbt.delete_node(popped_node.ride.rideNumber)
        output_add(popped_node.ride, "", False)
    else:
        output_add(None, "No active ride requests", False)

#cancel ride 
def cancel_ride(ride_number, heap, rbt):
    heap_node = rbt.delete_node(ride_number)
    if heap_node is not None:
        heap.delete_element(heap_node.min_heap_index)

#update ride for 3 conditions 
def update_ride(rideNumber, new_duration, heap, rbt):
    rbt_node = rbt.get_ride(rideNumber)
    if rbt_node is None:
        print("")
    elif new_duration <= rbt_node.ride.tripDuration:
        heap.update_element(rbt_node.min_heap_node.min_heap_index, new_duration)
    elif rbt_node.ride.tripDuration < new_duration <= (2 * rbt_node.ride.tripDuration):
        cancel_ride(rbt_node.ride.rideNumber, heap, rbt)
        insert_ride(Ride_model(rbt_node.ride.rideNumber, rbt_node.ride.rideCost + 10, new_duration), heap, rbt)
    else:
        cancel_ride(rbt_node.ride.rideNumber, heap, rbt)


if __name__ == "__main__":
    heap = MinHeap()
    rbt = RBTree()
    file = open("output_file.txt", "w")
    file.close()
    file = open("input.txt", "r")
    for s in file.readlines():
        n = []
        for num in s[s.index("(") + 1:s.index(")")].split(","):
            if num != '':
                n.append(int(num))
        if "Insert" in s:
            insert_ride(Ride_model(n[0], n[1], n[2]), heap, rbt)
        elif "Print" in s:
            if len(n) == 1:
                print_ride(n[0], rbt)
            elif len(n) == 2:
                print_rides(n[0], n[1], rbt)
        elif "UpdateTrip" in s:
            update_ride(n[0], n[1], heap, rbt)
        elif "GetNextRide" in s:
            get_next_ride(heap, rbt)
        elif "CancelRide" in s:
            cancel_ride(n[0], heap, rbt)

