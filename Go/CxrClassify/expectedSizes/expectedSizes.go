package expectedSizes

var Expected_sizes = map[string]int{
	"subset":   88320855,
	"full_set": 80694582486,
}

var Expected_num_files_in_dataset = map[string]int{
	"subset":   10,
	"full_set": 7468,
}

var SourceUrl = map[string]string{
	"subset":   "https://raw.githubusercontent.com/Matt-Conrad/CXR_View_Classification/master/datasets/NLMCXR_subset_dataset.tgz",
	"full_set": "https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz",
}

const loggerName string = "logger"
