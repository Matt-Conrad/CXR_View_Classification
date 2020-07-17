#ifndef EXPECTEDSIZES_H
#define EXPECTEDSIZES_H

#include <unordered_map>

const std::unordered_map<std::string, uint64_t> expected_sizes = {
        {"NLMCXR_subset_dataset.tgz", 88320855},
        {"NLMCXR_dcm.tgz", 80694582486}
    };

const std::unordered_map<std::string, uint16_t> expected_num_files_in_dataset = {
        {"NLMCXR_subset_dataset.tgz", 10},
        {"NLMCXR_dcm.tgz", 7470}
    };

const std::unordered_map<std::string, std::string> c_sourceUrl = {
        {"subset", "https://raw.githubusercontent.com/Matt-Conrad/CXR_View_Classification/master/datasets/NLMCXR_subset_dataset.tgz"},
        {"full_set", "https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz"}
    };

#endif // EXPECTEDSIZES_H
