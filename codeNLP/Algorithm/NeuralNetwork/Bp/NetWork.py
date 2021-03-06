# -*- coding: utf-8 -*-

# Write : lgy
# Data : 2017-09-24
# function: Algorithm class NetWork for bp network

from Connections import Connections
from Layer import Layer
from Connection import Connection

class NetWork(object):
	def __init__(self, layers):
		"""
		初始化一个全连接神经网络
		:param layers: 二维数组，描述神经网络每层节点数
		"""
		self.connections = Connections()
		self.layers = []
		layers_count = len(layers)
		node_count = 0
		for i in range(layers_count-1):
			self.layers.append(Layer(i,layers[i]))
		for layer in range(layers_count-1):
			connections = [Connection(upstream_node,downstream_node)
			               for upstream_node in self.layers[layer].nodes
							for downstream_node in self.layers[layer+1].nodes[:-1]]
			for conn in connections:
				self.connections.add_connection(conn)
				conn.downstream_node.append_upstream_connection(conn)
				conn.upstream_node.append_downstream_connection(conn)

	def train(self, data_set, labels, rate, iteration):
		"""
		训练神经网络
		:param data_set: 二维数组 训练样本的特征，每个元素是一个样本特征
		:param labels: 数组，训练样本标签。没个元素是一个样本的标签
		:param rate: 学习率
		:param iteration: 迭代次数
		:return:
		"""
		for i in range(iteration):
			for d in range(len(data_set)):
				self.train_one_sample(data_set[d],labels[d],rate)

	def train_one_sample(self, sample, label, rate):
		"""
		内部函数
		一次一个样本训练网络
		:param sample:
		:param label:
		:param rate:
		:return:
		"""
		self.predict(sample)
		self.calc_delta(label)
		self.update_weight(rate)

	def calc_delta(self, label):
		"""
		内部函数
		计算每个节点的delta
		:param label:
		:return:
		"""
		output_nodes = self.layers[-1].nodes
		for i in range(len(label)):
			output_nodes[i].calc_output_layer_delta(label[i])

		for layer in self.layers[-2::-1]:
			for node in layer:
				node.calc_hidden_layer_delta()

	def update_weight(self, rate):
		"""
		内部函数，
		更新每个连接权重
		:param rate:
		:return:
		"""
		for layer in self.layers[:-1]:
			for node in layer.nodes:
				for conn in node.downstream:
					conn.update_weight(rate)

	def calc_gradient(self):
		"""
		内部函数
		计算每个连接的梯度
		:return:
		"""
		for layer in self.layers[:-1]:
			for node in layer.nodes:
				for conn in node.downstream:
					conn.calc_gradient()

	def get_gradient(self, sample, label):
		"""
		获得网络在一个样本下，每个连接上的梯度
		:param sample: 样本输入
		:param label: 样本标签
		:return:
		"""
		self.predict(sample)
		self.calc_delta(label)
		self.calc_gradient()

	def predict(self, sample):
		"""
		根据输入样本预测输出值
		:param sample: 数组，样本的特征，也就是网络的输入向量
		:return:
		"""
		self.layers[0].set_output(sample)
		for i in range(1 , len(self.layers)):
			self.layers[i].calc_output()
		return map(lambda node : node.output, self.layers[-1].modes[:-1])

	def dump(self):
		"""
		打印网络信息
		:return:
		"""
		for layer in self.layers:
			layer.dump()