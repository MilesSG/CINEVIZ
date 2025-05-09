/**
 * 脚本用于修复电影海报URL映射和添加备用URL
 */
const fs = require('fs');
const path = require('path');

// 海报目录
const POSTERS_DIR = __dirname;

// 读取poster_map.json文件
let posterMap = {};
try {
  const posterMapPath = path.join(POSTERS_DIR, 'poster_map.json');
  if (fs.existsSync(posterMapPath)) {
    const content = fs.readFileSync(posterMapPath, 'utf8');
    posterMap = JSON.parse(content);
    console.log('读取到现有的poster_map.json文件');
  }
} catch (error) {
  console.error('读取poster_map.json文件失败:', error);
}

// 扫描posters目录，获取所有图片文件
const imageFiles = fs.readdirSync(POSTERS_DIR)
  .filter(file => {
    const ext = path.extname(file).toLowerCase();
    return ['.jpg', '.jpeg', '.png', '.webp', '.svg'].includes(ext);
  })
  .filter(file => file !== 'default-poster.svg');

console.log(`找到 ${imageFiles.length} 个图片文件`);

// 电影标题列表 - 确保与movies.js中的列表保持一致
const movieTitles = [
  '星际迷航', '赛博朋克', '流浪地球', '复仇者联盟', '速度与激情', 
  '蜘蛛侠：英雄远征', '哥斯拉', '金刚', '泰坦尼克号', '阿凡达', 
  '黑客帝国', '指环王', '哈利波特', '变形金刚', '加勒比海盗',
  '疯狂动物城', '寻梦环游记', '千与千寻', '龙猫', '你的名字',
  '楚门的世界', '肖申克的救赎', '盗梦空间', '星球大战', '霸王别姬',
  '这个杀手不太冷', '头号玩家', '鬼灭之刃', '未来水世界', '异形',
  '中国机长', '战狼', '长津湖', '我和我的祖国', '囧妈',
  '哪吒之魔童降世', '唐人街探案', '红海行动', '建国大业', '夏洛特烦恼'
];

// 外部可靠的备用URL映射
const backupUrls = {
  '星际迷航': 'https://img.enmuo.com/2017/12/27/15142736012633.jpg',
  '赛博朋克': 'https://img.enmuo.com/2018/11/29/15435179617654.jpg',
  '流浪地球': 'https://img.enmuo.com/2019/05/08/15573069518151.jpg',
  '复仇者联盟': 'https://img.enmuo.com/2018/05/24/15271560895430.jpg',
  '速度与激情': 'https://img.enmuo.com/2017/05/17/14950303417844.jpg',
  '蜘蛛侠：英雄远征': 'https://img.enmuo.com/2019/08/28/15669641326232.jpg',
  '哥斯拉': 'https://img.enmuo.com/2019/08/01/15647119728834.jpg',
  '金刚': 'https://img.enmuo.com/2018/05/16/15264986517911.jpg',
  '泰坦尼克号': 'https://img.enmuo.com/2018/03/27/15221658885967.jpg',
  '阿凡达': 'https://img.enmuo.com/2018/02/08/15180898513661.jpg',
  '黑客帝国': 'https://img.enmuo.com/2018/05/23/15270637717450.jpg',
  '指环王': 'https://img.enmuo.com/2018/05/16/15264999128559.jpg',
  '哈利波特': 'https://img.enmuo.com/2018/05/15/15264129327661.jpg',
  '变形金刚': 'https://img.enmuo.com/2018/05/15/15264068555830.jpg',
  '加勒比海盗': 'https://img.enmuo.com/2018/05/22/15269808197279.jpg',
  '疯狂动物城': 'https://img.enmuo.com/2018/05/22/15269764126640.jpg',
  '寻梦环游记': 'https://img.enmuo.com/2018/05/22/15269746025909.jpg',
  '千与千寻': 'https://img.enmuo.com/2018/03/06/15203315535687.jpg',
  '龙猫': 'https://img.enmuo.com/2018/05/22/15269742016639.jpg',
  '你的名字': 'https://img.enmuo.com/2017/08/22/15033963008466.jpg',
  '楚门的世界': 'https://img.enmuo.com/2017/12/12/15130351396026.jpg',
  '肖申克的救赎': 'https://img.enmuo.com/2018/05/16/15264938317142.jpg',
  '盗梦空间': 'https://img.enmuo.com/2018/05/15/15264118225780.jpg',
  '星球大战': 'https://img.enmuo.com/2018/05/30/15276673535711.jpg',
  '霸王别姬': 'https://img.enmuo.com/2018/03/27/15221650626325.jpg',
  '这个杀手不太冷': 'https://img.enmuo.com/2018/05/15/15264061876339.jpg',
  '头号玩家': 'https://img.enmuo.com/2018/05/15/15264069325892.jpg',
  '鬼灭之刃': 'https://img.enmuo.com/2020/11/05/16045848315344.jpg',
  '未来水世界': 'https://img.enmuo.com/2017/09/10/15049938205954.jpg',
  '异形': 'https://img.enmuo.com/2018/05/16/15264966517177.jpg',
  '中国机长': 'https://img.enmuo.com/2019/12/30/15776988816455.jpg',
  '战狼': 'https://img.enmuo.com/2018/05/15/15263999026175.jpg',
  '长津湖': 'https://img.enmuo.com/2022/02/15/16448691726673.jpg',
  '我和我的祖国': 'https://img.enmuo.com/2019/11/14/15736753718234.jpg',
  '囧妈': 'https://img.enmuo.com/2020/05/04/15886031913343.jpg',
  '哪吒之魔童降世': 'https://img.enmuo.com/2019/09/26/15695055018732.jpg',
  '唐人街探案': 'https://img.enmuo.com/2018/05/15/15264000696278.jpg',
  '红海行动': 'https://img.enmuo.com/2018/05/15/15264000116229.jpg',
  '建国大业': 'https://img.enmuo.com/2018/05/15/15263999726150.jpg',
  '夏洛特烦恼': 'https://img.enmuo.com/2018/05/15/15264000666273.jpg'
};

// 为每个电影标题创建映射
const newPosterMap = {};

movieTitles.forEach(title => {
  // 尝试找到匹配的图片文件
  const matchingFile = imageFiles.find(file => {
    const fileName = path.parse(file).name;
    return fileName === title;
  });

  if (matchingFile) {
    // 如果找到了匹配的图片文件，使用本地路径
    newPosterMap[title] = `/posters/${matchingFile}`;
    console.log(`使用本地图片: ${title} -> ${matchingFile}`);
  } else if (backupUrls[title]) {
    // 如果没有本地图片，但有备用URL，则使用备用URL
    newPosterMap[title] = backupUrls[title];
    console.log(`使用备用URL: ${title}`);
  } else {
    // 如果也没有备用URL，使用默认海报
    newPosterMap[title] = '/posters/default-poster.svg';
    console.log(`使用默认海报: ${title}`);
  }
});

// 合并新旧映射
const finalPosterMap = { ...posterMap, ...newPosterMap };

// 保存新的映射文件
const newMapPath = path.join(POSTERS_DIR, 'poster_map.json');
fs.writeFileSync(newMapPath, JSON.stringify(finalPosterMap, null, 2), 'utf8');

console.log(`已保存新的海报映射文件，包含 ${Object.keys(finalPosterMap).length} 个电影。`);

// 创建一个修改过的movies.js副本来使用这些URL
const createModifiedPosters = () => {
  const postersTemplate = [
    '/* 电影海报URL映射 - 自动生成 */',
    'export const moviePosterUrls = ' + JSON.stringify(finalPosterMap, null, 2),
    '',
    '/* 电影列表 */',
    'export const movieTitles = ' + JSON.stringify(movieTitles, null, 2),
    '',
    '/* 电影列表与海报URL对象 */',
    'export const moviesWithPosters = movieTitles.map(title => ({',
    '  title,',
    '  poster_url: moviePosterUrls[title] || "/posters/default-poster.svg"',
    '}))',
    ''
  ].join('\n');

  fs.writeFileSync(path.join(POSTERS_DIR, 'movie_posters.js'), postersTemplate, 'utf8');
  console.log('已创建movie_posters.js文件，可以在项目中导入使用');
};

createModifiedPosters();