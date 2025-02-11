#include <cmath>
#include <cstdlib>
#include <iostream>
#include <memory_resource>
#include <vector>

class TreeNode {
public:
  TreeNode *left;
  TreeNode *right;

  TreeNode(TreeNode *left, TreeNode *right) {
    this->left = left;
    this->right = right;
  }

  ~TreeNode() {
    // Delete not needed, because all nodes will be de-allocated in the pool
    // delete left;
    // delete right;
  }
};
TreeNode *build_tree(int nodes, std::pmr::monotonic_buffer_resource &pool) {
  if (nodes == 0) {
    return nullptr;
  }

  int nodes_left = nodes / 2;
  int nodes_right = nodes - nodes_left - 1;

  TreeNode *node =
      (TreeNode *)pool.allocate(sizeof(TreeNode), alignof(TreeNode));
  node->left = build_tree(nodes_left, pool);
  node->right = build_tree(nodes_right, pool);
  return node;
}

void count_at_depths(const TreeNode *tree, int depth,
                     std::vector<int> &target) {
  if (tree == nullptr) {
    return;
  }

  target[depth] += 1;
  count_at_depths(tree->left, depth + 1, target);
  count_at_depths(tree->right, depth + 1, target);
}

int main(int argc, const char **argv) {
  int nodes = std::atoi(argv[1]);
  int depth = (int)ceil(log2((double)nodes)) + 1;

  size_t pool_size = nodes * sizeof(TreeNode);
  std::pmr::monotonic_buffer_resource pool(pool_size);

  TreeNode *tree = build_tree(nodes, pool);
  std::vector<int> counts(depth);

  count_at_depths(tree, 0, counts);

  for (size_t i = 0; i < depth; i++) {
    std::cout << i << " " << counts[i] << std::endl;
  }

  pool.deallocate(tree, pool_size);

  return 0;
}