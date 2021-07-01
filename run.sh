#Only for local test runs
echo ""
echo ""
echo ""
echo "This is a test run"
echo ""
echo ""
echo ""
sleep 1

./shut-down.sh
docker build -t mutpy_dev .
docker run -d --name mutpy_dev mutpy_dev
docker logs mutpy_dev --follow
