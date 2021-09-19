from math import *
import statistics
import decimal
import os.path
import csv
import sys

# get a list of numbers from a csv file
def getNumberListFromOneLineCsv(file_name):
  sample = []
  with open(file_name, 'rb') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
      for aNumber in row:
        sample.append(int(aNumber))
      break
  return sample

# calculates Manhattan distance
def distance(si, mi):
  return fabs(si-mi)

sample = getNumberListFromOneLineCsv(sys.argv[1])
m = getNumberListFromOneLineCsv(sys.argv[2])

iteration_means = []
iteration_means.append(m)

# list of cluster for each iteration
clusters = []
mij_changes = True

# zero iterations
iteration_index = 0

# while means changes
while(mij_changes):

  clusters.append([])

  #show means
  x = 1
  print("selected means:")
  for mi in m:
    print("  m" + str(x)+" = " + str(mi))
    x += 1

  # for each value in sample
  for si in sample:
    list_distances_i = []
    # dictionary where Distance is the key and Cluster Position its value.
    distances_index_value = {}
    mi_position = 0
    # for each mean
    for mi in m:
      distance_i = distance(si, mi)
      print('D'+str(mi_position + 1)+' = |'+str(si)+' - '+str(mi)+'|')
      print('D'+str(mi_position + 1)+' = '+str(distance_i))
      distances_index_value[distance_i] = mi_position

      list_distances_i.append(distance_i)
      mi_position += 1

    list_distances_i_sorted = sorted(list_distances_i)
    distance_value_min = list_distances_i_sorted[0]

    print("minD = " + str(distance_value_min))

    # get current iteration k-cluster and add a sample
    if len(clusters) > 0 and len(clusters[iteration_index]) > 0:
      cluster_i = clusters[iteration_index]
      k_cluster = cluster_i[distances_index_value[distance_value_min]]
      k_cluster.append(si)
      cluster_i[distances_index_value[distance_value_min]] = k_cluster
      clusters[iteration_index] = cluster_i
    else:
      cluster_i = []
      cluster_i.append(si)

      k_cluster = [[] for z in range(len(m))]
      k_cluster[distances_index_value[distance_value_min]] = cluster_i
      clusters[iteration_index] = k_cluster

    # current cluster
    print("  current cluster:\n  "+str(clusters[len(clusters) - 1]))
    print("")

  # added means of this current iteration
  list_means = []
  for k_cluster in clusters[iteration_index]:
    list_means.append(round(statistics.mean(k_cluster),1))
  iteration_means.append(list_means)

  # replace last means...
  m = list_means

  iteration_index += 1

  # save in file
  save_file_content = ''
  save_row_index = 0
  for row in clusters[len(clusters) - 1]:
    for row_i in row:
      if save_row_index == 0:
        save_file_content = save_file_content + str(row_i)+',1,0,0\n'
      elif save_row_index == 1:
        save_file_content = save_file_content + '0,0,'+str(row_i)+',2\n'
    save_row_index = save_row_index + 1
  save_file = open('save'+str(iteration_index)+'.csv', 'w')
  save_file.write(save_file_content)
  save_file.close
  #print('--->should saved: '+str(clusters[len(clusters) - 1]))
  print('means at ' + str(iteration_index) + 'th iteration:')
  print('  ' + str(iteration_means[len(iteration_means) - 1]))
  print('')

  # compare current mean with first of list_means
  for i in range(len(iteration_means)-1, len(iteration_means)):
    iteration_means_i_0 = iteration_means[i-1]
    iteration_means_i = iteration_means[i]

    changes = False
    # compare current and last mean respectly
    for j in range(len(m)-1):
      mean_i_0 = iteration_means_i_0[j]
      mean_i = iteration_means_i[j]
      if round(mean_i,1) != round(mean_i_0,1):
        changes = True
        break
    if changes:
      break
    else:
      print('  finish because means not change!')
      mij_changes = False

print('')
print('results:\n')
k = 0
last_iteration_mean = iteration_means[len(iteration_means) - 1]
for mean in last_iteration_mean:
  last_cluster = clusters[len(clusters) - 1]
  cluster_k = last_cluster[k];
  print(' [' + str(k) + '] For mean ' + str(mean) + " its cluster is " + str(cluster_k))
  k += 1
print('')
