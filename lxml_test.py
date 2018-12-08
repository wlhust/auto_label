from lxml import etree, objectify
import os

def gen_txt(filename, h, w, c, xmin, xmax, ymin, ymax):
    E = objectify.ElementMaker(annotate=False)
    anno_tree = E.annotation(
        E.folder('5_paper_1'),
        E.filename(filename[-1]),
        E.path('5_paper_1/'+filename[-1]),
        E.source(
            E.database('Unknown'),
            # E.annotation('PASCAL VOC2007'),
            # E.image('flickr'),
            # E.flickrid("341012865")
        ),
        E.size(
            E.width(w),
            E.height(h),
            E.depth(c)
        ),
        E.segmented(0),
        E.object(
            E.name('5元人民币纸币'),
            E.pose('Unspecified'),
            E.truncated('0'),
            E.difficult('0'),
            E.bndbox(
                E.xmin(str(xmin)),
                E.ymin(str(ymin)),
                E.xmax(str(xmax)),
                E.ymax(str(ymax))
            )
        ),
    )
    etree.ElementTree(anno_tree).write(filename+".xml", pretty_print=True)

if __name__ == "__main__":
    gen_txt('./voc',100,100,3)